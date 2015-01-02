openerp.portal_user_image = function(instance) {
var _t = instance.web._t;
var QWeb = instance.web.qweb;
instance.web.WebClient.include({
    update_logo: function() {
        var company = this.session.company_id;
        var img = this.session.url('/portal_user_image/binary/company_logo' + (company ? '?company=' + company : '') + (this.session.uid ? '&user='+ this.session.uid : '' ));
        this.$('.oe_logo img').attr('src', '').attr('src', img);
        this.$('.oe_logo_edit').toggleClass('oe_logo_edit_admin', this.session.uid === 1);
    },
});
};