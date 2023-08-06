from __future__ import unicode_literals

import util

import datetime
import itertools

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager


# User models

@python_2_unicode_compatible
class Attendee(models.Model):
    ''' Miscellaneous user-related data. '''

    def __str__(self):
        return "%s" % self.user

    @staticmethod
    def get_instance(user):
        ''' Returns the instance of attendee for the given user, or creates
        a new one. '''
        try:
            return Attendee.objects.get(user=user)
        except ObjectDoesNotExist:
            return Attendee.objects.create(user=user)

    def save(self, *a, **k):
        while not self.access_code:
            access_code = util.generate_access_code()
            if Attendee.objects.filter(access_code=access_code).count() == 0:
                self.access_code = access_code
        return super(Attendee, self).save(*a, **k)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Badge/profile is linked
    access_code = models.CharField(
        max_length=6,
        unique=True,
        db_index=True,
    )
    completed_registration = models.BooleanField(default=False)
    guided_categories_complete = models.ManyToManyField("category")


class AttendeeProfileBase(models.Model):
    ''' Information for an attendee's badge and related preferences.
    Subclass this in your Django site to ask for attendee information in your
    registration progess.
     '''

    objects = InheritanceManager()

    @classmethod
    def name_field(cls):
        ''' This is used to pre-fill the attendee's name from the
        speaker profile. If it's None, that functionality is disabled. '''
        return None

    def invoice_recipient(self):
        ''' Returns a representation of this attendee profile for the purpose
        of rendering to an invoice. Override in subclasses. '''

        # Manual dispatch to subclass. Fleh.
        slf = AttendeeProfileBase.objects.get_subclass(id=self.id)
        # Actually compare the functions.
        if type(slf).invoice_recipient != type(self).invoice_recipient:
            return type(slf).invoice_recipient(slf)

        # Return a default
        return slf.attendee.user.username

    attendee = models.OneToOneField(Attendee, on_delete=models.CASCADE)


# Inventory Models

@python_2_unicode_compatible
class Category(models.Model):
    ''' Registration product categories, used as logical groupings for Products
    in registration forms.

    Attributes:
        name (str): The display name for the category.

        description (str): Some explanatory text for the category. This is
            displayed alongside the forms where your attendees choose their
            items.

        required (bool): Requires a user to select an item from this category
            during initial registration. You can use this, e.g., for making
            sure that the user has a ticket before they select whether they
            want a t-shirt.

        render_type (int): This is used to determine what sort of form the
            attendee will be presented with when choosing Products from this
            category. These may be either of the following:

            ``RENDER_TYPE_RADIO`` presents the Products in the Category as a
            list of radio buttons. At most one item can be chosen at a time.
            This works well when setting limit_per_user to 1.

            ``RENDER_TYPE_QUANTITY`` shows each Product next to an input field,
            where the user can specify a quantity of each Product type. This is
            useful for additional extras, like Dinner Tickets.

        limit_per_user (Optional[int]): This restricts the number of items
            from this Category that each attendee may claim. This extends
            across multiple Invoices.

        display_order (int): An ascending order for displaying the Categories
            available. By convention, your Category for ticket types should
            have the lowest display order.
    '''

    class Meta:
        verbose_name = _("inventory - category")
        verbose_name_plural = _("inventory - categories")
        ordering = ("order", )

    def __str__(self):
        return self.name

    RENDER_TYPE_RADIO = 1
    RENDER_TYPE_QUANTITY = 2

    CATEGORY_RENDER_TYPES = [
        (RENDER_TYPE_RADIO, _("Radio button")),
        (RENDER_TYPE_QUANTITY, _("Quantity boxes")),
    ]

    name = models.CharField(
        max_length=65,
        verbose_name=_("Name"),
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
    )
    limit_per_user = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Limit per user"),
        help_text=_("The total number of items from this category one "
                    "attendee may purchase."),
    )
    required = models.BooleanField(
        blank=True,
        help_text=_("If enabled, a user must select an "
                    "item from this category."),
    )
    order = models.PositiveIntegerField(
        verbose_name=("Display order"),
        db_index=True,
    )
    render_type = models.IntegerField(
        choices=CATEGORY_RENDER_TYPES,
        verbose_name=_("Render type"),
        help_text=_("The registration form will render this category in this "
                    "style."),
    )


@python_2_unicode_compatible
class Product(models.Model):
    ''' Registration products '''

    class Meta:
        verbose_name = _("inventory - product")
        ordering = ("category__order", "order")

    def __str__(self):
        return "%s - %s" % (self.category.name, self.name)

    name = models.CharField(
        max_length=65,
        verbose_name=_("Name"),
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_("Product category")
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    limit_per_user = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Limit per user"),
    )
    reservation_duration = models.DurationField(
        default=datetime.timedelta(hours=1),
        verbose_name=_("Reservation duration"),
        help_text=_("The length of time this product will be reserved before "
                    "it is released for someone else to purchase."),
    )
    order = models.PositiveIntegerField(
        verbose_name=("Display order"),
        db_index=True,
    )


@python_2_unicode_compatible
class Voucher(models.Model):
    ''' Registration vouchers '''

    # Vouchers reserve a cart for a fixed amount of time, so that
    # items may be added without the voucher being swiped by someone else
    RESERVATION_DURATION = datetime.timedelta(hours=1)

    def __str__(self):
        return "Voucher for %s" % self.recipient

    @classmethod
    def normalise_code(cls, code):
        return code.upper()

    def save(self, *a, **k):
        ''' Normalise the voucher code to be uppercase '''
        self.code = self.normalise_code(self.code)
        super(Voucher, self).save(*a, **k)

    recipient = models.CharField(max_length=64, verbose_name=_("Recipient"))
    code = models.CharField(max_length=16,
                            unique=True,
                            verbose_name=_("Voucher code"))
    limit = models.PositiveIntegerField(verbose_name=_("Voucher use limit"))


# Product Modifiers

@python_2_unicode_compatible
class DiscountBase(models.Model):
    ''' Base class for discounts. Each subclass has controller code that
    determines whether or not the given discount is available to be added to
    the current cart. '''

    objects = InheritanceManager()

    def __str__(self):
        return "Discount: " + self.description

    def effects(self):
        ''' Returns all of the effects of this discount. '''
        products = self.discountforproduct_set.all()
        categories = self.discountforcategory_set.all()
        return itertools.chain(products, categories)

    description = models.CharField(
        max_length=255,
        verbose_name=_("Description"),
        help_text=_("A description of this discount. This will be included on "
                    "invoices where this discount is applied."),
        )


@python_2_unicode_compatible
class DiscountForProduct(models.Model):
    ''' Represents a discount on an individual product. Each Discount can
    contain multiple products and categories. Discounts can either be a
    percentage or a fixed amount, but not both. '''

    def __str__(self):
        if self.percentage:
            return "%s%% off %s" % (self.percentage, self.product)
        elif self.price:
            return "$%s off %s" % (self.price, self.product)

    def clean(self):
        if self.percentage is None and self.price is None:
            raise ValidationError(
                _("Discount must have a percentage or a price."))
        elif self.percentage is not None and self.price is not None:
            raise ValidationError(
                _("Discount may only have a percentage or only a price."))

        prods = DiscountForProduct.objects.filter(
            discount=self.discount,
            product=self.product)
        cats = DiscountForCategory.objects.filter(
            discount=self.discount,
            category=self.product.category)
        if len(prods) > 1:
            raise ValidationError(
                _("You may only have one discount line per product"))
        if len(cats) != 0:
            raise ValidationError(
                _("You may only have one discount for "
                    "a product or its category"))

    discount = models.ForeignKey(DiscountBase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField()


@python_2_unicode_compatible
class DiscountForCategory(models.Model):
    ''' Represents a discount for a category of products. Each discount can
    contain multiple products. Category discounts can only be a percentage. '''

    def __str__(self):
        return "%s%% off %s" % (self.percentage, self.category)

    def clean(self):
        prods = DiscountForProduct.objects.filter(
            discount=self.discount,
            product__category=self.category)
        cats = DiscountForCategory.objects.filter(
            discount=self.discount,
            category=self.category)
        if len(prods) != 0:
            raise ValidationError(
                _("You may only have one discount for "
                    "a product or its category"))
        if len(cats) > 1:
            raise ValidationError(
                _("You may only have one discount line per category"))

    discount = models.ForeignKey(DiscountBase, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    percentage = models.DecimalField(
        max_digits=4,
        decimal_places=1)
    quantity = models.PositiveIntegerField()


class TimeOrStockLimitDiscount(DiscountBase):
    ''' Discounts that are generally available, but are limited by timespan or
    usage count. This is for e.g. Early Bird discounts. '''

    class Meta:
        verbose_name = _("discount (time/stock limit)")
        verbose_name_plural = _("discounts (time/stock limit)")

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Start time"),
        help_text=_("This discount will only be available after this time."),
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("End time"),
        help_text=_("This discount will only be available before this time."),
    )
    limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Limit"),
        help_text=_("This discount may only be applied this many times."),
    )


class VoucherDiscount(DiscountBase):
    ''' Discounts that are enabled when a voucher code is in the current
    cart. '''

    class Meta:
        verbose_name = _("discount (enabled by voucher)")
        verbose_name_plural = _("discounts (enabled by voucher)")

    voucher = models.OneToOneField(
        Voucher,
        on_delete=models.CASCADE,
        verbose_name=_("Voucher"),
        db_index=True,
    )


class IncludedProductDiscount(DiscountBase):
    ''' Discounts that are enabled because another product has been purchased.
    e.g. A conference ticket includes a free t-shirt. '''

    class Meta:
        verbose_name = _("discount (product inclusions)")
        verbose_name_plural = _("discounts (product inclusions)")

    enabling_products = models.ManyToManyField(
        Product,
        verbose_name=_("Including product"),
        help_text=_("If one of these products are purchased, the discounts "
                    "below will be enabled."),
    )


class RoleDiscount(object):
    ''' Discounts that are enabled because the active user has a specific
    role. This is for e.g. volunteers who can get a discount ticket. '''
    # TODO: implement RoleDiscount
    pass


@python_2_unicode_compatible
class FlagBase(models.Model):
    ''' This defines a condition which allows products or categories to
    be made visible, or be prevented from being visible.

    The various subclasses of this can define the conditions that enable
    or disable products, by the following rules:

    If there is at least one 'disable if false' flag defined on a product or
    category, all such flag conditions must be met. If there is at least one
    'enable if true' flag, at least one such condition must be met.

    If both types of conditions exist on a product, both of these rules apply.
    '''

    class Meta:
        # TODO: make concrete once https://code.djangoproject.com/ticket/26488
        # is solved.
        abstract = True

    DISABLE_IF_FALSE = 1
    ENABLE_IF_TRUE = 2

    def __str__(self):
        return self.description

    def effects(self):
        ''' Returns all of the items affected by this condition. '''
        return itertools.chain(self.products.all(), self.categories.all())

    @property
    def is_disable_if_false(self):
        return self.condition == FlagBase.DISABLE_IF_FALSE

    @property
    def is_enable_if_true(self):
        return self.condition == FlagBase.ENABLE_IF_TRUE

    description = models.CharField(max_length=255)
    condition = models.IntegerField(
        default=ENABLE_IF_TRUE,
        choices=(
            (DISABLE_IF_FALSE, _("Disable if false")),
            (ENABLE_IF_TRUE, _("Enable if true")),
        ),
        help_text=_("If there is at least one 'disable if false' flag "
                    "defined on a product or category, all such flag "
                    " conditions must be met. If there is at least one "
                    "'enable if true' flag, at least one such condition must "
                    "be met. If both types of conditions exist on a product, "
                    "both of these rules apply."
        ),
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        help_text=_("Products affected by this flag's condition."),
        related_name="flagbase_set",
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        help_text=_("Categories whose products are affected by this flag's "
                    "condition."
        ),
        related_name="flagbase_set",
    )


class EnablingConditionBase(FlagBase):
    ''' Reifies the abstract FlagBase. This is necessary because django
    prevents renaming base classes in migrations. '''
    # TODO: remove this, and make subclasses subclass FlagBase once
    # https://code.djangoproject.com/ticket/26488 is solved.

    objects = InheritanceManager()


class TimeOrStockLimitFlag(EnablingConditionBase):
    ''' Registration product ceilings '''

    class Meta:
        verbose_name = _("flag (time/stock limit)")
        verbose_name_plural = _("flags (time/stock limit)")

    start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Products included in this condition will only be "
                    "available after this time."),
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Products included in this condition will only be "
                    "available before this time."),
    )
    limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_("The number of items under this grouping that can be "
                    "purchased."),
    )


@python_2_unicode_compatible
class ProductFlag(EnablingConditionBase):
    ''' The condition is met because a specific product is purchased. '''

    class Meta:
        verbose_name = _("flag (dependency on product)")
        verbose_name_plural = _("flags (dependency on product)")

    def __str__(self):
        return "Enabled by products: " + str(self.enabling_products.all())

    enabling_products = models.ManyToManyField(
        Product,
        help_text=_("If one of these products are purchased, this condition "
                    "is met."),
    )


@python_2_unicode_compatible
class CategoryFlag(EnablingConditionBase):
    ''' The condition is met because a product in a particular product is
    purchased. '''

    class Meta:
        verbose_name = _("flag (dependency on product from category)")
        verbose_name_plural = _("flags (dependency on product from category)")

    def __str__(self):
        return "Enabled by product in category: " + str(self.enabling_category)

    enabling_category = models.ForeignKey(
        Category,
        help_text=_("If a product from this category is purchased, this "
                    "condition is met."),
    )


@python_2_unicode_compatible
class VoucherFlag(EnablingConditionBase):
    ''' The condition is met because a Voucher is present. This is for e.g.
    enabling sponsor tickets. '''

    class Meta:
        verbose_name = _("flag (dependency on voucher)")
        verbose_name_plural = _("flags (dependency on voucher)")

    def __str__(self):
        return "Enabled by voucher: %s" % self.voucher

    voucher = models.OneToOneField(Voucher)


# @python_2_unicode_compatible
class RoleFlag(object):
    ''' The condition is met because the active user has a particular Role.
    This is for e.g. enabling Team tickets. '''
    # TODO: implement RoleFlag
    pass


# Commerce Models

@python_2_unicode_compatible
class Cart(models.Model):
    ''' Represents a set of product items that have been purchased, or are
    pending purchase. '''

    class Meta:
        index_together = [
            ("active", "time_last_updated"),
            ("active", "released"),
            ("active", "user"),
            ("released", "user"),
        ]

    def __str__(self):
        return "%d rev #%d" % (self.id, self.revision)

    user = models.ForeignKey(User)
    # ProductItems (foreign key)
    vouchers = models.ManyToManyField(Voucher, blank=True)
    time_last_updated = models.DateTimeField(
        db_index=True,
    )
    reservation_duration = models.DurationField()
    revision = models.PositiveIntegerField(default=1)
    active = models.BooleanField(
        default=True,
        db_index=True,
    )
    released = models.BooleanField(
        default=False,
        db_index=True
    )  # Refunds etc

    @classmethod
    def reserved_carts(cls):
        ''' Gets all carts that are 'reserved' '''
        return Cart.objects.filter(
            (Q(active=True) &
                Q(time_last_updated__gt=(
                    timezone.now()-F('reservation_duration')
                                        ))) |
            (Q(active=False) & Q(released=False))
        )


@python_2_unicode_compatible
class ProductItem(models.Model):
    ''' Represents a product-quantity pair in a Cart. '''

    class Meta:
        ordering = ("product", )

    def __str__(self):
        return "product: %s * %d in Cart: %s" % (
            self.product, self.quantity, self.cart)

    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField(db_index=True)


@python_2_unicode_compatible
class DiscountItem(models.Model):
    ''' Represents a discount-product-quantity relation in a Cart. '''

    class Meta:
        ordering = ("product", )

    def __str__(self):
        return "%s: %s * %d in Cart: %s" % (
            self.discount, self.product, self.quantity, self.cart)

    cart = models.ForeignKey(Cart)
    product = models.ForeignKey(Product)
    discount = models.ForeignKey(DiscountBase)
    quantity = models.PositiveIntegerField()


@python_2_unicode_compatible
class Invoice(models.Model):
    ''' An invoice. Invoices can be automatically generated when checking out
    a Cart, in which case, it is attached to a given revision of a Cart. '''

    STATUS_UNPAID = 1
    STATUS_PAID = 2
    STATUS_REFUNDED = 3
    STATUS_VOID = 4

    STATUS_TYPES = [
        (STATUS_UNPAID, _("Unpaid")),
        (STATUS_PAID, _("Paid")),
        (STATUS_REFUNDED, _("Refunded")),
        (STATUS_VOID, _("VOID")),
    ]

    def __str__(self):
        return "Invoice #%d" % self.id

    def clean(self):
        if self.cart is not None and self.cart_revision is None:
            raise ValidationError(
                "If this is a cart invoice, it must have a revision")

    @property
    def is_unpaid(self):
        return self.status == self.STATUS_UNPAID

    @property
    def is_void(self):
        return self.status == self.STATUS_VOID

    @property
    def is_paid(self):
        return self.status == self.STATUS_PAID

    @property
    def is_refunded(self):
        return self.status == self.STATUS_REFUNDED

    # Invoice Number
    user = models.ForeignKey(User)
    cart = models.ForeignKey(Cart, null=True)
    cart_revision = models.IntegerField(
        null=True,
        db_index=True,
    )
    # Line Items (foreign key)
    status = models.IntegerField(
        choices=STATUS_TYPES,
        db_index=True,
    )
    recipient = models.CharField(max_length=1024)
    issue_time = models.DateTimeField()
    due_time = models.DateTimeField()
    value = models.DecimalField(max_digits=8, decimal_places=2)


@python_2_unicode_compatible
class LineItem(models.Model):
    ''' Line items for an invoice. These are denormalised from the ProductItems
    and DiscountItems that belong to a cart (for consistency), but also allow
    for arbitrary line items when required. '''

    class Meta:
        ordering = ("id", )

    def __str__(self):
        return "Line: %s * %d @ %s" % (
            self.description, self.quantity, self.price)

    invoice = models.ForeignKey(Invoice)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    product = models.ForeignKey(Product, null=True, blank=True)


@python_2_unicode_compatible
class PaymentBase(models.Model):
    ''' The base payment type for invoices. Payment apps should subclass this
    class to handle implementation-specific issues. '''

    class Meta:
        ordering = ("time", )

    objects = InheritanceManager()

    def __str__(self):
        return "Payment: ref=%s amount=%s" % (self.reference, self.amount)

    invoice = models.ForeignKey(Invoice)
    time = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)


class ManualPayment(PaymentBase):
    ''' Payments that are manually entered by staff. '''
    pass


class CreditNote(PaymentBase):
    ''' Credit notes represent money accounted for in the system that do not
    belong to specific invoices. They may be paid into other invoices, or
    cashed out as refunds.

    Each CreditNote may either be used to pay towards another Invoice in the
    system (by attaching a CreditNoteApplication), or may be marked as
    refunded (by attaching a CreditNoteRefund).'''

    @classmethod
    def unclaimed(cls):
        return cls.objects.filter(
            creditnoteapplication=None,
            creditnoterefund=None,
        )

    @property
    def status(self):
        if self.is_unclaimed:
            return "Unclaimed"

        if hasattr(self, 'creditnoteapplication'):
            destination = self.creditnoteapplication.invoice.id
            return "Applied to invoice %d" % destination

        elif hasattr(self, 'creditnoterefund'):
            reference = self.creditnoterefund.reference
            print reference
            return "Refunded with reference: %s" % reference

        raise ValueError("This should never happen.")

    @property
    def is_unclaimed(self):
        return not (
            hasattr(self, 'creditnoterefund') or
            hasattr(self, 'creditnoteapplication')
        )

    @property
    def value(self):
        ''' Returns the value of the credit note. Because CreditNotes are
        implemented as PaymentBase objects internally, the amount is a
        negative payment against an invoice. '''
        return -self.amount


class CleanOnSave(object):

    def save(self, *a, **k):
        self.full_clean()
        super(CleanOnSave, self).save(*a, **k)


class CreditNoteApplication(CleanOnSave, PaymentBase):
    ''' Represents an application of a credit note to an Invoice. '''

    def clean(self):
        if not hasattr(self, "parent"):
            return
        if hasattr(self.parent, 'creditnoterefund'):
            raise ValidationError(
                "Cannot apply a refunded credit note to an invoice"
            )

    parent = models.OneToOneField(CreditNote)


class CreditNoteRefund(CleanOnSave, models.Model):
    ''' Represents a refund of a credit note to an external payment.
    Credit notes may only be refunded in full. How those refunds are handled
    is left as an exercise to the payment app. '''

    def clean(self):
        if not hasattr(self, "parent"):
            return
        if hasattr(self.parent, 'creditnoteapplication'):
            raise ValidationError(
                "Cannot refund a credit note that has been paid to an invoice"
            )

    parent = models.OneToOneField(CreditNote)
    time = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=255)


class ManualCreditNoteRefund(CreditNoteRefund):
    ''' Credit notes that are entered by a staff member. '''

    entered_by = models.ForeignKey(User)
