import json
from ebid.models import *
from django.conf import settings
from datetime import datetime, date, time
from django.http import HttpResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from datetime import datetime, timedelta
from ebid.forms import *
from django.contrib.auth.forms import AuthenticationForm
import pytz
LOGIN_PATH = '/login/'
WAITING_TIME = timedelta(minutes = 5)
BUFFER_TIME = timedelta(minutes = 1)

def time_left(bid):
   end_ = 0

   if bid.closing_date:
      print "bid",bid.closing_date, "now", datetime.now().replace(tzinfo=pytz.timezone("Asia/Manila"))
      end_ = bid.closing_date - datetime.now().replace(tzinfo=pytz.timezone("Asia/Manila"))

      end_ = end_.seconds
      print end_
      if end_ < 0:
         end_ = 0

   return end_

def home(request):
   return render(request, 'home.html')

def history(request):
   return

def login(request):
   """
   Displays the login form and handles the login action.
   """
   print request.POST
   def redirectIfNext(redirectPath):
      try:
         redirectNext = request.session.pop("login_next")
      except KeyError:
         return redirect(redirectPath)
      return redirect(redirectNext)

   if request.user.is_authenticated():
      return redirectIfNext('/dashboard')

   if request.method == 'POST':
      form = AuthenticationForm(request,data=request.POST)
      if form.is_valid():
         user = authenticate(username=request.POST['username'], password=request.POST['password'])
         if user is not None:
            if user.is_active:
               django_login(request, user)
          
               return redirectIfNext('/dashboard')
   else:
      if 'next' in request.GET:
         request.session['login_next'] = request.GET.get('next')
      form = AuthenticationForm(request)
   return render_to_response('dashboard/login.html', {
         'form': form,
          }, context_instance=RequestContext(request))

@login_required(login_url=LOGIN_PATH)
def dashboard(request):
   if request.user.acct_type == 'S':
      return redirect("/dashboard/live_bidding/")
   return render(request, 'dashboard/home.html')

def new_bidding(request):
   if request.method == "POST":
      user = request.user
      form = NewBiddingForm( data=request.POST)
      if form.is_valid():
         bi = BidInformation(
            org = user.org,
            bid_title = form.cleaned_data['title'],
            description = form.cleaned_data['description'],
            classification = form.cleaned_data['classification'],
            business_category = form.cleaned_data['business_category'],
            procurement_mode = form.cleaned_data['procurement_mode'],
            approved_budget = form.cleaned_data['budget'],
            contact_person = form.cleaned_data['contact_person'],
            contact_person_address = form.cleaned_data['contact_address'],
            reason = form.cleaned_data['reason']
            )
         bi.save()

         return redirect('/dashboard/new_bidding/?id='+str(bi.id))
   else:
      bi = BidInformation.objects.get(id=request.GET.get('id'))
      vars_ = [("Title", bi.bid_title),("Description", bi.description),("Classification", bi.classification),
                  ("Category", bi.business_category),("Mode", bi.procurement_mode),
                  ("Budget", bi.approved_budget),("Contact Person", bi.contact_person),("Contact Address", bi.contact_person_address),
                 ("Reason", bi.reason),("Bidders", bi.getBidders())]
      
      tl =  time_left(bi)
      if tl == 0 and bi.stage == 1:
         bi.stage = 2
         bi.save()

      gg = {"status_": bi.getStatus(),
         "vars":vars_,"bidinfo_id":bi.id,
         'status': bi.stage,
         'timeleft':tl}
      return render(request, 'dashboard/new_bidding.html', 
         gg
         )

def fetch_biditems(request):
   try:
      response = []
      bid = BidInformation.objects.get(id=request.GET.get('id'))
      bid_items = bid.bidlineitem_set.all().order_by('item_no')

      for bi in bid_items:
         response.append([bi.id, bi.item_no, bi.name, bi.description, bi.quantity, bi.uom, bi.budget])

      print response
      return HttpResponse(json.dumps(response), content_type="application/json")

   except Exception, e:
      import logging
      logging.exception(e)
      raise e

# fetch the current bid ranking for this
def fetch_bids(request):
   print "fetch bids"
   try:
      bid = BidInformation.objects.get(id=request.GET.get('id'))
      items = BidLineItem.objects.filter(bid_parent=bid)
      response = []

      for item in items:
         allbids = BidInstance.objects.filter(biditem=item)
         mybids = allbids.filter(org=request.user.org).order_by('-time')

         if len(mybids) > 0:
            mybid = mybids[0]
            myrank = 1
            for bid_ in allbids:
               if bid_.budget < mybid.budget:
                  myrank +=1
            response.append([item.item_no, item.name, item.quantity, mybid.budget, myrank])
         else:
            response.append([item.item_no, item.name, item.quantity, "--", "--"])
      print response
      return HttpResponse(json.dumps(response), content_type="application/json")
   except Exception, e:
      import logging
      logging.exception(e)
#user now bids
def do_bid(request):
   response = {'status':'failed'}
   try:
      bid = BidInformation.objects.get(id=request.POST.get('bid_id'))
      bid_item = BidLineItem.objects.get(id=request.POST.get('bid_item_id'))
      budget = float(request.POST.get('bid_budget'))

      if bid.stage == '1' and bid.closing_date > datetime.now().replace(tzinfo=pytz.timezone("Asia/Manila")):
         BidInstance(bidinfo=bid, biditem=bid_item, org = request.user.org, budget=budget).save()
         response['status'] = 'success'
         print "bid success"

         print time_left(bid), BUFFER_TIME, "xxxxx" 
         if time_left(bid) <= BUFFER_TIME and time_left > 0:
            bid.closing_date = datetime.now().replace(tzinfo=pytz.timezone("Asia/Manila")) + timedelta(minutes=BUFFER_TIME)
            bid.save()

      else:
         print "CANNOT BID, CLOSED"
   except Exception, e:
      import logging
      logging.exception(e)

   return HttpResponse(json.dumps(response),content_type='application/json')

def add_bidder(request):
   response = {}
   try:
      user = request.user
      bid = BidInformation.objects.get(id=request.GET.get('id'))
      to_add = BiddersList(org=user.org, bidinfo=bid)
      to_add.save()

      response['status'] = 'success'
      print "OK"
   except Exception, e:
      response['status'] = 'failed'
      import logging
      logging.exception(e)

   return HttpResponse(json.dumps(response), content_type="application/json")

def add_biditem(request):
   response = {"status":"success"}
   
   try:
      print "id",request.POST.get('id')
      bid = BidInformation.objects.get(id=request.POST.get('id'))
      bid_items = bid.bidlineitem_set.all().order_by('item_no')
      bid_lineitem = BidLineItem(
         bid_parent = bid,
         item_no = len(bid_items),
         description = request.POST.get('description'),
         quantity = request.POST.get('qty'),
         uom = request.POST.get('uom'),
         budget = request.POST.get('budget'),
         name = request.POST.get('name')
      )

      bid_lineitem.save()
      response['id'] = bid_lineitem.id
      print response
   except Exception, e:
      import logging
      logging.exception(e)
      response['status'] = 'failed'

   return HttpResponse(json.dumps(response), content_type='application/json')

def remove_biditem(request):
   return 

@login_required(login_url=LOGIN_PATH)
def live_bidding(request):
   return render(request, 'dashboard/live_bidding.html')

def live_bidding_new(request):
   my_org = request.user.org

   if request.method == 'GET':
      bid = BidInformation.objects.get(id=request.GET.get('id'))
      bidderslist = BiddersList.objects.filter(bidinfo=bid, org=my_org)
      
      print bidderslist
      if len(bidderslist) == 1:
         bidder = True
      else:
         bidder = False

      try:
         bi = BidInformation.objects.get(id=request.GET.get('id'))
      except Exception, e:
         raise e

      vars_ = [("Title", bi.bid_title),("Description", bi.description),("Classification", bi.classification),
                     ("Category", bi.business_category),("Mode", bi.procurement_mode),
                     ("Budget", bi.approved_budget),("Contact Person", bi.contact_person),("Contact Address", bi.contact_person_address),("Reason", bi.reason),
                     ("Status", bi.getStatus()), ("Bidders", bi.getBidders())]

      return render(request,'dashboard/live_bidding_view.html', {'bi':bid,'info':vars_, 'bidder':bidder, 'acct_type': request.user.acct_type, 'status': bi.stage})

   elif request.method == 'POST':
      try:
         bid = BidInformation.objects.get(id=request.POST.get('id'))
         bid_instance = BidInstance.objects.filter(bidinfo = bid).values('biditem')


      except Exception, e:
         raise e

def publish_bid(request):
   try:
      bid = BidInformation.objects.get(id=request.POST.get('id'))
      bid.stage = '1'
      bid.publish_date = datetime.now().replace(tzinfo=pytz.timezone("Asia/Manila"))
      bid.closing_date = datetime.now().replace(tzinfo=pytz.timezone("Asia/Manila")) + WAITING_TIME
      bid.save()

      response = {'status': 'success'}
   except Exception, e:
      import logging
      logging.exception(e)
      response = {'status': 'failed'}
   print response
   return HttpResponse(json.dumps(response), content_type="application/json")

def bid_info(request):
   try:
      bidid = request.GET.get('id')
      bid = BidInformation.objects.get(id=bidid)
   
#      bid_list = BiddersList.object.filter(bid=).order_by('')
   except Exception, e:
      raise e


def user_profile(request):
   return 

def fetch_live_bids(request):
   print "fetch_live_bids  "
   import pytz
   my_org = request.user.org
   try:
      response = []
      bids = BidInformation.objects.order_by('-creation_date')
      for bid in bids:
         if bid.org == my_org:
            mybid = True
         else:
            mybid = False

         end_ = time_left(bid)
         if end_ == 0 and bid.stage == 1:
            bid.stage = 2
            bid.save()

         to_add = [bid.id, bid.bid_title, bid.org.org_name, bid.classification, bid.approved_budget, 0, bid.stage, mybid, end_]
         response.append(to_add)
      print response
      return HttpResponse(json.dumps(response), content_type="application/json")

   except Exception, e:
      import logging
      logging.exception(e)
