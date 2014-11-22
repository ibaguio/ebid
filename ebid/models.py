from django.db import models

class Organization(models.Model):
	"""Description of Supplier/Agency"""
	member_type = models.CharField(max_length=255)
	parent_org_id = models.IntegerField()
	is_org_foreign = models.BooleanField(default=False)
	org_name = models.CharField(max_length=255)
	government_branch = models.CharField(max_length=255)
	government_organization_type = models.CharField(max_length=255)
	supplier_form_of_organization = models.CharField(max_length=255)
	supplier_organization_type = models.CharField(max_length=255)
	org_reg_date = models.DateTimeField(auto_now_add=True)
	website = models.CharField(max_length=255)
	org_description = models.TextField()
	country_code = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	region = models.CharField(max_length=255)
	province = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	address1 = models.CharField(max_length=255)
	address2 = models.CharField(max_length=255)
	address3 = models.CharField(max_length=255)
	zip_code = models.CharField(max_length=255)
	org_status = models.BooleanField(default=False)
	modified_date = models.DateTimeField(auto_now=True)
	
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
	line_item = models.ForeignKey('BidLineItem', null=True)
	item_name = models.CharField(max_length=255)
	item_description = models.TextField()
	qty = models.IntegerField()
	uom = models.CharField(max_length=255) #unit of measurement
	unspsc_code = models.CharField(max_length=255)
	unspsc_description = models.CharField(max_length=255)
	budget = models.BigIntegerField()
	awardee = models.ForeignKey(Organization) 		# organization the bid was awarded
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
	stage = models.CharField(max_length=255)
	stage2_ref_id = models.CharField(max_length=255)
	org = models.ForeignKey(Organization) #im guessing this is the entity that made the bidding
	classification = models.CharField(max_length=255)
	solicitation_no = models.CharField(max_length=255)
	notice_type = models.CharField(max_length=255)
	business_category = models.CharField(max_length=255)
	procurement_mode = models.CharField(max_length=255)
	funding_instrument = models.CharField(max_length=255)
	funding_source = models.CharField(max_length=255)
	approved_budget = models.CharField(max_length=255)
	publish_date = models.DateTimeField()
	closing_date = models.DateTimeField()
	contact_duration = models.CharField(max_length=255)
	calendar_type = models.CharField(max_length=255)
	trade_agreement = models.CharField(max_length=255)
	pre_bid_date = models.DateTimeField()
	pre_bid_venue = models.CharField(max_length=255)
	procuring_entity_org = models.ForeignKey(Organization,related_name="procuring_entity_org")
	client_agency_org = models.ForeignKey(Organization,related_name="client_agency_org")
	contact_person = models.CharField(max_length=255)
	contact_person_address = models.CharField(max_length=255)
	bid_title = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	others_info = models.CharField(max_length=255)
	reason = models.CharField(max_length=255)
	created_by = models.CharField(max_length=255)
	creation_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	location = models.CharField(max_length=255) #project location
	modified_date = models.DateTimeField(auto_now=True)

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
	award = models.ForeignKey(Award)
	item = models.ForeignKey(BidLineItem)
	org = models.ForeignKey(Organization)
