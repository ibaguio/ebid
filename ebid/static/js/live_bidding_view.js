$(document).ready(function() {
    var BidItemObject = function(id, no, name, description, qty, uom, budget) {
        var self = this;
        self.id = ko.observable(id);
        self.no = ko.observable(no);
        self.name = ko.observable(name);
        self.description = ko.observable(description);
        self.qty = ko.observable(qty);
        self.uom = ko.observable(uom);
        self.budget = ko.observable(budget);

        if (status_ != '1'){
            self.bidme_btn = "Bidding closed";
        }else{
        self.bidme_btn = "<a href='#'>Bid</a>";
        }
        self.bidme = function(row_){
            if (status_ == '1'){
                var x = window.prompt("Your bid for "+self.name());
                var data = {
                    bid_id:bidinfo_id,
                    bid_item_id:row_.id(),
                    bid_budget:x,
                }
                console.log(data);
                $.ajax("/dashboard/live_bidding/do_bid/", {
                    type: 'post',
                    data: data,
                    dataType: 'json',
                    beforeSend: function(xhr, settings){
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val())
                    },
                    success: function(data) {
                        if (data['status'] == 'failed'){
                            // self.addMessage(html);
                        } else {
                            location.reload();
                            // self.addMessage("New Bid Item added.");
                        }
                    },error: function(data){
                        // self.addMessage("Error: see logs.");
                    }
                });

            }
        }
    }

    var BidObject = function(no, name, qty, mybid, myrank) {
        var self = this;
        self.no = ko.observable(no);
        self.name = ko.observable(name);
        self.qty = ko.observable(qty);
        self.mybid = ko.observable(mybid);
        self.myrank = ko.observable(myrank);

    }

    var BidViewModel = function() {
        var self = this;
        self.bids = ko.observableArray([]);
        self.biditems = ko.observableArray([]);
        self.getBidsAJAX = function() {
            $.getJSON("/cgi/fetch_bids/?id="+bidinfo_id, function(data) {
                $.each(data, function(key, value) {
                    self.bids.push(new BidObject(value[0],value[1],value[2],value[3],value[4]));
                });
            });
        }
        self.getBidsAJAX();

        self.row_click = function(row_){
            if (row_.mybid() == true)
                var win = window.open('/dashboard/new_bidding/?id='+row_.id(),'_blank');
            else
                var win = window.open('/dashboard/live_bidding/view/?id='+row_.id(),'_blank');
            win.focus();
        }


        self.getBidItemAJAX = function() {
            self.owners = ko.observableArray([]);
            var el = $(".box-body");
            App.blockUI(el);
            $.getJSON("/dashboard/new_bidding/biditems/?id="+bidinfo_id, function(data) {
                $.each(data, function(key, value) {
                    self.biditems.push(new BidItemObject(value[0],value[1],value[2],value[3],value[4],value[5],value[6]));
                });
                App.unblockUI(el);
            });
        };
        self.getBidItemAJAX();

        self.addBidder = function(){
            $.getJSON("/dashboard/new_bidding/add_bidder/?id="+bidinfo_id, function(data) {
                if (data['status'] == 'succes'){
                    location.reload();
                }
                App.unblockUI(el);
            });
        }
    }
    uvm = new BidViewModel();
    ko.applyBindings(uvm);
});