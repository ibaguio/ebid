$(document).ready(function() {
    var BidObject = function(id, title_, proc_entity, class_, budget, bidders, status_,mybid, end) {
        var self = this;
        self.id = ko.observable(id);
        self.title_ = ko.observable(title_);
        self.proc_entity = ko.observable(proc_entity);
        self.class_ = ko.observable(class_);
        self.budget = ko.observable(budget);
        self.bidder = ko.observable(bidders);
        self.status_number = ko.observable(status_);
        self.mybid = ko.observable(mybid)
        
        // if (end > 0){
        //     self.timer = ko.observable(end);
        //     self.minutes = ko.computed( function() {
        //         return "Ends in: ("+ (Math.floor(self.timer() / 60) % 60).toString() + ":";
        //     }, self);

        //     self.seconds = ko.computed( function() {
        //         return (self.timer() % 60 ).toString() +")" ;
        //     }, self);

        //     setInterval(function() {
        //         var newTimer = self.timer() -1;
        //         self.timer(newTimer <= 0 ? 60 : newTimer);
        //         console.log(self.timer())
        //         if (self.timer() == 0) location.reload()
        //     }, 1000);
        // }else{
            self.minutes = "";
            self.seconds = "";
        // }

        if (status_ == '0'){
            self.status_ = ko.observable('PRE BID');
        }else if (status_ == '1'){
            self.status_ = ko.observable('LIVE');
        }else if (status_ == '2'){
            self.status_ =  ko.observable('DONE');
        }
    }

    var BidViewModel = function() {
        var self = this;
        self.bids = ko.observableArray([]);
        self.biditems = ko.observableArray([]);
        self.getBidsAJAX = function() {
            $.getJSON("/cgi/fetch_live_bids/", function(data) {
                $.each(data, function(key, value) {
                    self.bids.push(new BidObject(value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8]));
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


    }
    uvm = new BidViewModel();
    ko.applyBindings(uvm);
});