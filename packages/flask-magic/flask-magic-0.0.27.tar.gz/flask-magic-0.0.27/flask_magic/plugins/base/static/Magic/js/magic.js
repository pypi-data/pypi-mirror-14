
var Magic = {

    /**
    Google Analytics tracking
    **/
    track_event: function(category, action, label, value) {
        if (typeof ga !== 'undefined') {
            ga("send", "event", category, action, label, value)
        }
    },

    //------

    /**
    BASIC Login
    **/
    basic_login: function() {
        var that = this
        $("#magic-login-login-form").submit(function(e){
            e.preventDefault();
            that.track_event("User", "LOGIN", "Email")
            this.submit()
        })
        $("#magic-login-signup-form").submit(function(e){
            e.preventDefault();
            that.track_event("User", "SIGNUP", "Email")
            this.submit()
        })
        $("#magic-login-lostpassword-form").submit(function(e){
            e.preventDefault();
            that.track_event("User", "LOSTPASSWORD", "Email")
            this.submit()
        })
    },

    /**
     * Setup Authomatic
     */
    setup_authomatic: function(redirect) {
        authomatic.setup({
            onLoginComplete: function(result) {
                switch(result.custom.action) {
                    case "redirect":
                        location.href = result.custom.url
                        break
                    default:
                        if (redirect == "") {
                            redirect = "/"
                        }
                        location.href = redirect
                        break
                }
            }
        })

        authomatic.popupInit()
    },

    Widget: {
        /**
         * A function that launch a modal and return a callback to access the clicked element
         * @param el
         * @param callback
         */
        onModalShow: function(el, callback) {
            $(el).on("show.bs.modal").on('show.bs.modal', function (event) {
                var button = $(event.relatedTarget) // Button that triggered the modal
                var modal = $(this)
                callback(button, modal)
            })

        } ,
        parseWidgetModalContent: function() {
           /**
            * WIDGET-MODAL
            * Modal Hook to add the header and footer in the modal dynamically
            *
            * Add the tag header or footer in the content of the modal so it properly
            * place the content in modal-header and modal-footer respectively.
            *
            * Requirements:
            *   The modal must have the class 'widget-modal'
            *
            * Add either <header> or <footer> or both in the body
            *
            * <header> My New Title</header>
            *
            * <footer>Buttons here</footer>
            */
           $(".widget-modal").each(function(){
                var el = $(this);
                var header = el.find(".modal-content header");
                var footer = el.find(".modal-content footer");
                var form = el.find("form");
                if (header.length > 0) {
                    el.find(".modal-header").html(header);
                }
                if (footer.length > 0) {
                    el.find(".modal-content").append(
                            $("<div/>", {"class": "modal-footer"}).append(footer)
                    )
                }
               if (form.length > 0) {
                   el.find('footer [type="submit"]').on("click", function(){
                       form.submit()
                   })
               }
            })
        },
         parseWidgetPanelContent: function() {
           /**
            * WIDGET-PANEL
            * Modal Hook to add the header and footer in the panel dynamically
            *
            * Add the tag header or footer in the content of the modal so it properly
            * place the content in panel-heading and panel-footer respectively.
            *
            * Requirements:
            *   The panel must have the class 'widget-panel'
            *
            * Add either <header> or <footer> or both in the body
            *
            * <header> My New Title</header>
            *
            * <footer>Buttons here</footer>
            */
           $(".widget-panel").each(function(){
                var el = $(this);
                var header = el.find(".panel-body header");
                var footer = el.find(".panel-body footer");
                var form = el.find("form");
                if (header.length > 0) {
                    el.find(".panel-heading").html(header);
                }
                if (footer.length > 0) {
                    el.find(".panel-body").append(
                            $("<div/>", {"class": "panel-footer"}).append(footer)
                    )
                }
               if (form.length > 0) {
                   el.find('footer [type="submit"]').on("click", function(){
                       form.submit()
                   })
               }
            })
        }
    },

    /**
     * @deprecated
     */
    onModalShow: function(el, callback) {
        this.Widget.onModalShow(el,  callback)

    },


    init: function() {

        // Lazy load images
        $("img.lazy").lazy({
            effect: "fadeIn",
            effectTime: 1000
        })

        // Oembed
        $("a.oembed").oembed(null, {
            includeHandle: false,
            maxWidth: "100%",
            maxHeight: "480",
        });

        // Share buttons
        $(".widget-share-buttons").each(function(){
            var el = $(this)
            el.jsSocials({
                url: el.data("url"),
                text: el.data("text"),
                showCount: el.data("show-count"),
                showLabel: el.data("show-label"),
                shares:el.data("buttons"),
                _getShareUrl: function() {
                    var url = jsSocials.Socials.prototype._getShareUrl.apply(this, arguments);
                    var width = 550;
                    var height = 420;
                    var winHeight = screen.height, winWidth = screen.width;
                    var left = Math.round((winWidth / 2) - (width / 2));
                    var top = (winHeight > height) ? Math.round((winHeight / 2) - (height / 2)) : 0;
                    var options = "scrollbars=yes,resizable=yes,toolbar=no,location=yes" + ",width=" + width + ",height=" + height + ",left=" + left + ",top=" + top;
                    return "javascript:window.open('" + url + "', 'Sharing', '"+ options +"')";
                }
            });

        })

        // form validator
        $.validate({
            modules : 'security'
        });

        this.Widget.parseWidgetModalContent();
        //this.Widget.parseWidgetPanelContent();

    }
}


$(function(){
    Magic.init()
})