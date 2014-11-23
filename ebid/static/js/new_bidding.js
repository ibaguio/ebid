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
    }

    var BidItemViewModel = function() {
        var self = this;
        self.biditems = ko.observableArray([]);

        self.new_no = ko.observable();
        self.new_name = ko.observable();
        self.new_description = ko.observable();
        self.new_qty = ko.observable();
        self.new_uom = ko.observable();
        self.new_budget = ko.observable();

        self.addMessage = ko.observable();
        self.message = ko.observable();
        self.validationStatus = ko.observable();

        
        if (time_left > 0){
            self.timer = ko.observable(time_left);
            self.minutes = ko.computed( function() {
                return "Ends in: ("+ (Math.floor(self.timer() / 60) % 60).toString() + ":";
            }, self);

            self.seconds = ko.computed( function() {
                return (self.timer() % 60 ).toString() +")" ;
            }, self);

            setInterval(function() {
                var newTimer = self.timer() -1;
                self.timer(newTimer <= 0 ? 60 : newTimer);
                if (self.timer == 0) location.reload()
            }, 1000);
        }else{
            self.minutes = "";
            self.seconds = "";
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

        self.addBidItem = function() {
            var data = {
                id: bidinfo_id,
                no: self.new_no(),
                name: self.new_name(),
                description: self.new_description(),
                qty: self.new_qty(),
                uom: self.new_uom(),
                budget: self.new_budget()
            };
            $.ajax("/dashboard/new_bidding/add_biditem/", {
                type: 'post',
                data: data,
                dataType: 'json',
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val())
                },
                success: function(data) {
                    if (data['status'] == 'failed'){
                        self.validationStatus('fail');
                        errors = data['error'];
                        html="";
                        for (var err in errors){
                            $("input#"+err).parent().addClass('has-error');
                            html+="<b>"+err+":</b> "+errors[err]+"<br />";
                        }
                        self.addMessage(html);
                    } else {
                        self.validationStatus('success');
                        self.biditems.push(new BidItemObject(data['id'],self.new_no(),self.new_name(),self.new_description(),self.new_qty(),self.new_uom(), self.new_budget()));
                        self.new_no("");
                        self.new_name("");
                        self.new_description("");
                        self.new_qty("");
                        self.addMessage("New Bid Item added.");
                        self.reinitializeTable();
                        $("input").parent().removeClass('has-error');
                    }
                },error: function(data){
                    self.validationStatus('fail');
                    self.addMessage("Error: see logs.");
                }
            });
        };

        self.removeBidLine = function(bidline) {
            if (confirm("Are you sure you want to delete " + bidline.name() + "?")) {
                $.ajax("/dashboard/new_bidding/remove_bidline/", {
                    type: 'post',
                    data: { id: bidline.id() },
                    dataType: 'json',
                    beforeSend: function(xhr, settings){
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val())
                    },
                    success: function (data) {
                        if (data['status'] == 'ok') {
                            self.validationStatus('success');
                            self.message("<strong>Success!</strong><b>" + bidline.name() + "</b> removed. <a href='javascript:window.location.reload()'>Refresh</a> page to see changes.");
                        }
                    }
                });
            }
        }.bind(self);

        self.publish = function(){
            var data = {
                id: bidinfo_id
            }
            $.ajax("/dashboard/new_bidding/publish/", {
                type: 'post',
                data: data,
                dataType: 'json',
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                },
                success: function(data) {
                    if (data['status'] == 'failed'){
                        alert("Failed to make bid live");
                    }else{
                        window.location = '/dashboard/live_bidding/';
                    }
                }, error: function(data){
                    alert("Failed to make bid live");
                }
            });
        }.bind(self);

        self.clearAlerts = function() {
            $("input").parent().removeClass('has-error');
            self.message("");
            self.addMessage("");
            self.new_no("");
            self.new_name("");
            self.new_description("");
            self.new_qty("");
            self.new_uom("");
            self.new_budget("");
        };
   
    }
    ivm = new BidItemViewModel();
    ko.applyBindings(ivm);
});