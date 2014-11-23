$(document).ready(function() {
    var InventoryObject = function(id,tracking_no,model,serial_no,mac_addr) {
        var self = this;
        self.id = ko.observable(id);
        self.tracking_no = ko.observable(tracking_no);
        self.model = ko.observable(model);
        self.serial_no = ko.observable(serial_no);
        self.mac_addr = ko.observable(mac_addr);
    }

    var InventoryViewModel = function() {
        var self = this;
        self.inventory = ko.observableArray([]);
        self.new_tracking_no = ko.observable();
        self.new_model = ko.observable();
        self.new_serial_no = ko.observable();
        self.new_mac_addr = ko.observable();
        
        self.addMessage = ko.observable();
        self.message = ko.observable();
        self.validationStatus = ko.observable();

        self.selectedInventory = ko.observable(new InventoryObject('None','None','None','None','None'));
        self.owners = ko.observableArray([]);
        self.selectedOwners = ko.observableArray([]);
        self.activate = ko.observable(false);

        self.nasid = ko.observable();
        self.readable_name = ko.observable();
        self.location = ko.observable();
        self.description = ko.observable();
        self.longitude = ko.observable();
        self.latitude = ko.observable();

        self.toggleActivate = function (stock) {
            self.activate(true);
            self.selectedInventory(stock);
        };

        self.getInventoryAJAX = function() {
            self.owners = ko.observableArray([]);
            var el = $(".box-body");
            App.blockUI(el);
            $.getJSON("/cgi/inventory/", function(data) {
                $.each(data['aps'], function(key, value) {
                    self.inventory.push(new InventoryObject(value['id'],value['tracking_no'],value['model'],value['serial_no'],value['mac_addr']));
                });
                self.owners(data['owner'])
                self.reinitializeTable();
                $(".multiselect").multiselect({
                    numberDisplayed: 8,
                    maxHeight: 200,
                    enableCaseInsensitiveFiltering: true,
                    includeSelectAllOption: true,
                    buttonClass: 'form-control'
                });
                App.unblockUI(el);
            });
        };
        self.getInventoryAJAX();

        self.addStock = function() {
            var data = {
                tracking_no: self.new_tracking_no(),
                model: self.new_model(),
                serial_no: self.new_serial_no(),
                mac_addr: self.new_mac_addr()
            };
            $.ajax("/dashboard/inventory/add/", {
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
                        self.inventory.push(new InventoryObject(data['id'],self.new_tracking_no(),self.new_model(),self.new_serial_no(),self.new_mac_addr()));
                        self.new_tracking_no("");
                        self.new_model("");
                        self.new_serial_no("");
                        self.new_mac_addr("");
                        self.addMessage("New inventory added.");
                        self.reinitializeTable();
                        $("input").parent().removeClass('has-error');
                    }
                },error: function(data){
                    self.validationStatus('fail');
                    self.addMessage("Error: see logs.");
                }
            });
        };

        self.removeStock = function(stock) {
            if (confirm("Are you sure you want to delete stock with tracking no. " + stock.tracking_no() + "?")) {
                $.ajax("/dashboard/inventory/remove/", {
                    type: 'post',
                    data: { id: stock.id() },
                    dataType: 'json',
                    beforeSend: function(xhr, settings){
                        xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val())
                    },
                    success: function (data) {
                        if (data['status'] == 'ok') {
                            self.validationStatus('success');
                            self.message("<strong>Success!</strong> Access Point stock with tracking no. <b>" + stock.tracking_no() + "</b> removed. <a href='javascript:window.location.reload()'>Refresh</a> page to see changes.");
                            //self.inventory.remove(stock);
                            //$("#inventory").dataTable().fnDestroy();
                            //self.reinitializeTable();
                        }
                    }
                });
            }
        }.bind(self);

        self.activateStock = function(stock) {
            var data = {
                id: self.selectedInventory().id(),
                name: self.nasid(),
                readable_name: self.readable_name(),
                location: self.location(),
                description: self.description(),
                owner: self.selectedOwners(),
                longitude: self.longitude(),
                latitude: self.latitude()
            };
            $.ajax("/dashboard/inventory/activate/", {
                type: 'post',
                data: data,
                dataType: 'json',
                beforeSend: function(xhr, settings){
                    xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val())
                },
                success: function(data) {
                    if (data['status'] == 'ok') {
                        self.validationStatus('success');
                        self.nasid("");
                        self.readable_name("");
                        self.location("");
                        self.description("");
                        self.selectedOwners([]);
                        self.longitude("");
                        self.latitude("");
                        self.activate(false);
                        self.message("<strong>Success!</strong> Stock AP activated. <a href='javascript:window.location.reload()'>Refresh</a> page to see changes.");
                        //self.inventory.remove(stock);
                        //$("#inventory").dataTable().fnDestroy();
                        //self.reinitializeTable();
                    } else {
                        self.validationStatus('fail');
                        errors = data['error'];
                        html="";
                        for (var err in errors){
                            html+="<b>"+err+":</b> "+errors[err]+"<br />";
                        }
                        self.message(html);
                    }
                }
            });
        }

        self.clearAlerts = function() {
            $("input").parent().removeClass('has-error');
            self.message("");
            self.addMessage("");
            self.new_tracking_no("");
            self.new_model("");
            self.new_serial_no("");
            self.new_mac_addr("");
        };
    }
    ivm = new InventoryViewModel();
    ko.applyBindings(ivm);
})