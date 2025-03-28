/** @odoo-module **/

//import { patch } from "@web/core/utils/patch";
//import { PosStore } from "@point_of_sale/app/store/pos_store";
//patch(PosStore.prototype, {
//   getReceiptHeaderData() {
//       return {
//           ...super.getReceiptHeaderData(...arguments),
//           partner: this.get_order().get_partner(),
//       };
//   },
//});

import { Order } from '@point_of_sale/app/store/models';
import { patch } from '@web/core/utils/patch';

patch( Order.prototype,{
    export_for_printing(){
        const result = super.export_for_printing(...arguments );

        if( this.get_partner() ){
            result.headerData.partner = this.get_partner();
        }
        return result;
    }
});
