from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Organization(models.Model):
   """Description of Supplier/Agency"""
   member_type = models.CharField(max_length=255, null=True, blank=True)
   parent_org = models.ForeignKey('Organization', null=True, blank=True)
   is_org_foreign = models.BooleanField(default=False)
   org_name = models.CharField(max_length=255)
   government_branch = models.CharField(max_length=255, null=True, blank=True)
   government_organization_type = models.CharField(max_length=255, null=True, blank=True)
   supplier_form_of_organization = models.CharField(max_length=255, null=True, blank=True)
   supplier_organization_type = models.CharField(max_length=255, null=True, blank=True)
   org_reg_date = models.DateTimeField(auto_now_add=True)
   website = models.CharField(max_length=255, null=True, blank=True)
   org_description = models.TextField(null=True, blank=True)
   country_code = models.CharField(max_length=255, null=True, blank=True)
   country = models.CharField(max_length=255, null=True, blank=True)
   region = models.CharField(max_length=255, null=True, blank=True)
   province = models.CharField(max_length=255, null=True, blank=True)
   city = models.CharField(max_length=255, null=True, blank=True)
   address1 = models.CharField(max_length=255, null=True, blank=True)
   address2 = models.CharField(max_length=255, null=True, blank=True)
   address3 = models.CharField(max_length=255, null=True, blank=True)
   zip_code = models.CharField(max_length=255, null=True, blank=True)
   org_status = models.CharField(max_length=128, null=True, blank=True)
   modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

   def __unicode__(self):
      return self.org_name
   
class Award(models.Model):
   """Final awarded bids"""
   STATUS_CHOICES = (
      ('U','Updated'),
      ('P','Posted'),
   )

   AWARD_TYPE = (
      ('AN','Award Notice'),
      ('NP','Negotiated Procurement'),#Negotiated Procurement (Adjacent / Contiguous)
   )

   award_id = models.IntegerField()
   ref_id = models.IntegerField()
   title = models.CharField(max_length=255)
   reason = models.CharField(max_length=255)
   status = models.CharField(max_length=1, choices=STATUS_CHOICES)
   publish_date = models.DateTimeField()
   previous_award_id = models.IntegerField()
   line_item = models.ForeignKey('BidLineItem', null=True, blank=True)
   item_name = models.CharField(max_length=255)
   item_description = models.TextField()
   qty = models.IntegerField()
   uom = models.CharField(max_length=255) #unit of measurement
   unspsc_code = models.CharField(max_length=255)
   unspsc_description = models.CharField(max_length=255)
   budget = models.BigIntegerField()
   awardee = models.ForeignKey(Organization)       # organization the bid was awarded
   award_type = models.CharField(max_length=3, choices=AWARD_TYPE)
   contract_amt = models.BigIntegerField()
   award_date = models.DateTimeField()
   award_reason = models.CharField(max_length=255)
   contract_no = models.CharField(max_length=255)
   proceed_date = models.DateTimeField()
   contract_start_date = models.DateTimeField()
   contract_enddate = models.DateTimeField()
   is_short_list = models.BooleanField(default=False)
   is_reaward = models.BooleanField(default=False)
   is_amp = models.BooleanField(default=False)
   modified_date = models.DateTimeField(auto_now=True)

class BidInformation(models.Model):
   """Bid records"""
   #ref_no deprecated 
   stage = models.CharField(max_length=1, default = '0')
   stage2_ref_id = models.CharField(max_length=255, blank=True)
   org = models.ForeignKey(Organization) #im guessing this is the entity that made the bidding
   classification = models.CharField(max_length=255,null=True, blank=True)
   solicitation_no = models.CharField(max_length=255,null=True, blank=True)
   notice_type = models.CharField(max_length=255,null=True, blank=True)
   business_category = models.CharField(max_length=255,null=True, blank=True)
   procurement_mode = models.CharField(max_length=255,null=True, blank=True)
   funding_instrument = models.CharField(max_length=255,null=True, blank=True)
   funding_source = models.CharField(max_length=255,null=True, blank=True)
   approved_budget = models.CharField(max_length=255,null=True, blank=True)
   publish_date = models.DateTimeField(null=True, blank=True)
   closing_date = models.DateTimeField(null=True, blank=True)
   contact_duration = models.CharField(max_length=255,null=True, blank=True)
   calendar_type = models.CharField(max_length=255,null=True, blank=True)
   trade_agreement = models.CharField(max_length=255,null=True, blank=True)
   pre_bid_date = models.DateTimeField(null=True, blank=True)
   pre_bid_venue = models.CharField(max_length=255,blank=True)
   procuring_entity_org = models.ForeignKey(Organization,related_name="procuring_entity_org",blank=True, null=True)
   client_agency_org = models.ForeignKey(Organization,related_name="client_agency_org",blank=True, null=True)
   contact_person = models.CharField(max_length=255,null=True, blank=True)
   contact_person_address = models.CharField(max_length=255,null=True, blank=True)
   bid_title = models.CharField(max_length=255)
   description = models.CharField(max_length=255)
   others_info = models.CharField(max_length=255,null=True, blank=True)
   reason = models.CharField(max_length=255,null=True, blank=True)
   created_by = models.CharField(max_length=255,null=True, blank=True)
   creation_date = models.DateTimeField(auto_now_add=True)
   modified_date = models.DateTimeField(auto_now=True)

   location = models.CharField(max_length=255,null=True, blank=True) #project location

   def getStatus(self):
      if self.stage == '0':
         return 'Pre Bid'
      elif self.stage == '1':
         return 'Live'
      else:
         return 'Finished'

   def getBidders(self):
      r = []
      b = BiddersList.objects.filter(bidinfo=self).values('org')
      for gg in b:

         r.append(Organization.objects.get(id=gg['org']).org_name)
      return "; ".join(r)

class BidLineItem(models.Model):
   bid_parent = models.ForeignKey(BidInformation)
   item_no = models.IntegerField()
   name = models.CharField(max_length=255)
   description  = models.CharField(max_length=255)
   quantity = models.IntegerField()
   uom = models.CharField(max_length=255) #unit of measurement
   budget = models.BigIntegerField()

   class Meta:
      unique_together = ('bid_parent','item_no')

class BiddersList(models.Model):
   # award = models.ForeignKey(Award)
   # item = models.ForeignKey(BidLineItem)
   org = models.ForeignKey(Organization)
   bidinfo = models.ForeignKey(BidInformation)
   approved = models.BooleanField(default=False)
   
   def __unicode__(self):
      return "%s %s %s"%(self.org, self.bidinfo.bid_title, self.approved)

   class Meta:
      unique_together = ('org', 'bidinfo')

class BidInstance(models.Model):
   bidinfo = models.ForeignKey(BidInformation)
   biditem = models.ForeignKey(BidLineItem)
   time = models.DateTimeField(auto_now_add=True)
   org = models.ForeignKey(Organization)
   budget = models.FloatField()

   def __unicode__(self):
      return "%s; %s; %s; %s"%(self.bidinfo.bid_title, self.biditem.name, self.org.org_name, self.budget)
#
# Custom User Modules
#
class MyUserManager(BaseUserManager):
   """
   Custom User manager for creating User and superuser.
   """
   def create_user(self, username, email, password=None):
      """
      Creates and saves a User with the given username, email,
      and password.
      """
      if not username:
         raise ValueError('Users must have a username')

      user = self.model(
         username=username,
         email=self.normalize_email(email),
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

   def create_superuser(self, username, email, password):
      """
      Creates and saves a superuser with the given username, email,
      and password.
      """
      user = self.create_user(username,
         password=password,
         email=email
      )
      user.acct_type = 'A'
      user.save(using=self._db)
      return user

class MyUser(AbstractBaseUser):
   """
   A custom User model with admin-compliant permissions.
   """

   USER_TYPE = (
      ('A','Admin'),
      ('G','Government'),
      ('S','Supplier')
   )

   username = models.CharField(max_length=32, unique=True)
   email = models.EmailField(verbose_name='email address',max_length=255,unique=True)
   first_name = models.CharField(max_length=30, blank=True)
   last_name = models.CharField(max_length=30, blank=True)
   contact = models.CharField(max_length=30, blank=True)
   location = models.CharField(max_length=100, blank=True)
   joined = models.DateTimeField(auto_now_add=True)
   acct_type = models.CharField(max_length=1, choices=USER_TYPE)
   org = models.ForeignKey(Organization, null=True, blank=True, default=None)

   objects = MyUserManager()

   USERNAME_FIELD = 'username'
   REQUIRED_FIELDS = ['email']

   def get_full_name(self):
      """
      Returns the first_name plus the last_name, with a space in between.
      """
      full_name = '%s %s' % (self.first_name, self.last_name)
      return full_name.strip()

   def get_short_name(self):
      """
      Returns the first_name for the user.
      """
      return self.first_name

   def __unicode__(self):
      return self.username

   def has_perm(self, perm, obj=None):
      """"
      Does the user have a specific permission?
      """
      # Simplest possible answer: Yes, always
      return True

   def has_module_perms(self, app_label):
      """
      Does the user have permissions to view the app `app_label`?
      """
      # Simplest possible answer: Yes, always
      return True

   @property
   def is_staff(self):
        """
        Is the user a member of staff?
        """
        # Simplest possible answer: All admins are staff
        return self.is_admin

   @property
   def is_admin(self):
      return self.acct_type == 'A'

   def is_govt(self):
      return self.acct_type == 'G'

   def is_supplier(self):
      return self.acct_type == 'S'