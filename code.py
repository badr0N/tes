def generate_xlsx_report(self, workbook, data, wizard):
      for doc in wizard:            
          docs = []
          datas = []
          dpl_obj = self.env['suntech.daily.delivery.requisition']
          bso_obj = self.env['suntech.blanket.sale.order']
          picking_obj = self.env['stock.picking']
          sale_obj = self.env['sale.order']
          purchase_obj = self.env['purchase.order']
          product_obj = self.env['product.product']
          bom_obj = self.env['mrp.bom']
          bom_line_obj = self.env['mrp.bom.line']
          stock_obj = self.env['stock.quant']
          stock_move_obj = self.env['stock.move.line']

          date = doc.date
          date_end = doc.date_end
          date_first = date_end.strftime('%Y-%m-01')
          date_first_format = datetime.strptime(date_first, '%Y-%m-%d')
          date_one_format = date_first_format + relativedelta(months=1)
          date_two_format = date_one_format + relativedelta(months=1)
          date_three_format = date_two_format + relativedelta(months=1)
          date_four_format = date_three_format + relativedelta(months=1)
          date_five_format = date_four_format + relativedelta(months=1)
          date_six_format = date_five_format + relativedelta(months=1)

          jit_start_date = datetime(date.year, date.month, date.day, 0, 0, 0, 0)
          jit_end_date_use = datetime(date_end.year, date_end.month, date_end.day, 23, 59, 59)    
          jit_end_date_one_delivery_use = jit_end_date_use + relativedelta(months=1)

          jit_date_end = datetime(date_end.year, date_end.month, 1, 23, 59, 59)
          jit_end_date_one_delivery = jit_date_end + relativedelta(months=1)
          jit_end_date = jit_date_end + relativedelta(months=2)

          bso_range_date = jit_date_end + relativedelta(months=1)

          bso_start_date = datetime(date.year, date.month, 1, 0, 0, 0, 0)
          bso_end_date = bso_start_date + relativedelta(months=6)

          if doc.category == 'so':
              dpl_ids = dpl_obj.search([('date_delivery', '>=', jit_start_date), ('date_delivery', '<=', jit_end_date), ('state', '!=', 'cancel')])
              product_ids = dpl_ids.mapped('ddr_ids.product_id.id')
              bso_ids = bso_obj.search([('contract_start', '>=', bso_start_date), ('contract_start', '<=', bso_end_date)])
              product_ids.extend(bso_ids.mapped('blanket_ids.product_id.id'))
              picking_ids = picking_obj.search([('scheduled_date', '>=', jit_start_date),('scheduled_date', '<=', jit_end_date_one_delivery), ('is_pick_so', '=', True), ('is_manual_do', '=', False), ('state', '=', 'done')])
              product_ids.extend(picking_ids.mapped('move_ids_without_package.product_id.id'))
              sale_ids = sale_obj.search([('state', '!=', 'cancel')])
              product_ids.extend(sale_ids.mapped('order_line.product_id.id'))
              purchase_ids = purchase_obj.search([('state', '=', 'purchase')])
              product_ids.extend(purchase_ids.mapped('order_line.product_id.id'))
              product_ids = set(product_ids)
              product_ids = product_obj.browse(product_ids).ids

              mrp_bom_obj = bom_obj.search([('product_id','in', product_ids), ('active', '=', True)])
              product_bom = mrp_bom_obj.mapped('components_line_ids')
              components = bom_line_obj.search([('id','in', product_bom.ids)], order='product_id asc')
              component = components.filtered(lambda r:  r.component_type_secondary == 'metal' or r.component_type in ['resin', 'mb', 'needle', 'pigment', 'metal'])               

          elif doc.category == 'customerso':
              if doc.is_st_plastics == True:
                  dpl_ids = dpl_obj.search([('date_delivery', '>=', jit_start_date), ('date_delivery', '<=', jit_end_date), ('shipping_address', '=', doc.shipping_id.id), ('state', '!=', 'cancel')])
                  product_ids = dpl_ids.mapped('ddr_ids.product_id.id')
                  bso_ids = bso_obj.search([('contract_start', '>=', bso_start_date), ('contract_start', '<=', bso_end_date), ('shipping_address_id', '=', doc.shipping_id.id)])
                  product_ids.extend(bso_ids.mapped('blanket_ids.product_id.id'))
                  picking_ids = picking_obj.search([('scheduled_date', '>=', jit_start_date),('scheduled_date', '<=', jit_end_date_one_delivery), ('shipping_address', '=', doc.shipping_id.id), ('is_pick_so', '=', True), ('is_manual_do', '=', False), ('state', '=', 'done')])
                  product_ids.extend(picking_ids.mapped('move_ids_without_package.product_id.id'))
                  sale_ids = sale_obj.search([('partner_id', '=', doc.shipping_id.id), ('state', '!=', 'cancel')])
                  product_ids.extend(sale_ids.mapped('order_line.product_id.id'))
                  product_cust_ids = product_obj.search([('partner_id', '=', doc.shipping_id.id)])
                  product_ids.extend(product_cust_ids.mapped('id'))
                  purchase_ids = purchase_obj.search([('state', '=', 'purchase')])
                  product_ids.extend(purchase_ids.mapped('order_line.product_id.id'))
                  product_ids = set(product_ids)
                  product_ids = product_obj.browse(product_ids).ids
                  
                  mrp_bom_obj = bom_obj.search([('product_id','in', product_ids), ('active', '=', True)])
                  product_bom = mrp_bom_obj.mapped('components_line_ids')
                  components = bom_line_obj.search([('id','in', product_bom.ids)], order='product_id asc')
                  component = components.filtered(lambda r:  r.component_type_secondary == 'metal' or r.component_type in ['resin', 'mb', 'needle', 'pigment', 'metal'])
              else:
                  dpl_ids = dpl_obj.search([('date_delivery', '>=', jit_start_date), ('date_delivery', '<=', jit_end_date), ('partner_id', '=', doc.partner_id.id), ('state', '!=', 'cancel')])
                  product_ids = dpl_ids.mapped('ddr_ids.product_id.id')
                  bso_ids = bso_obj.search([('contract_start', '>=', bso_start_date), ('contract_start', '<=', bso_end_date), ('partner_id', '=', doc.partner_id.id)])
                  product_ids.extend(bso_ids.mapped('blanket_ids.product_id.id'))
                  picking_ids = picking_obj.search([('scheduled_date', '>=', jit_start_date),('scheduled_date', '<=', jit_end_date_one_delivery), ('partner_id', '=', doc.partner_id.id), ('is_pick_so', '=', True), ('is_manual_do', '=', False), ('state', '=', 'done')])
                  product_ids.extend(picking_ids.mapped('move_ids_without_package.product_id.id'))
                  sale_ids = sale_obj.search([('partner_id', '=', doc.partner_id.id), ('state', '!=', 'cancel')])
                  product_ids.extend(sale_ids.mapped('order_line.product_id.id'))
                  purchase_ids = purchase_obj.search([('state', '=', 'purchase')])
                  product_ids.extend(purchase_ids.mapped('order_line.product_id.id'))
                  product_cust_ids = product_obj.search([('partner_id', '=', doc.partner_id.id)])
                  product_ids.extend(product_cust_ids.mapped('id'))
                  product_ids = set(product_ids)
                  product_ids = product_obj.browse(product_ids).ids
                  
                  mrp_bom_obj = bom_obj.search([('product_id','in', product_ids), ('active', '=', True)])
                  product_bom = mrp_bom_obj.mapped('components_line_ids')
                  components = bom_line_obj.search([('id','in', product_bom.ids)], order='product_id asc')
                  component = components.filtered(lambda r:  r.component_type_secondary == 'metal' or r.component_type in ['resin', 'mb', 'needle', 'pigment', 'metal'])

          title_parent = workbook.add_format({'font_size':16,'align': 'left', 'valign': 'vleft', })
          
          title = workbook.add_format({'border':1, 'align': 'center', 'valign': 'vcenter', 'font_size':8})
          table_center = workbook.add_format({'align': 'center','border':1, 'font_size':9})

          sheet = workbook.add_worksheet()            

          sheet.set_column('A:A', 20)
          sheet.set_column('B:B', 30)
          sheet.set_column('C:C', 35)
          sheet.set_column('D:D', 10)
          sheet.set_column('E:E', 20)
          sheet.set_column('F:F', 20)
          sheet.set_column('G:G', 20)
          sheet.set_column('H:H', 20)
          sheet.set_column('I:I', 20)
          sheet.set_column('J:J', 20)
          sheet.set_column('K:K', 20)
          sheet.set_column('L:L', 20)
          sheet.set_column('M:M', 20)
          sheet.set_column('N:N', 30)
          sheet.set_column('O:O', 20)
          sheet.set_column('P:P', 30)
          sheet.set_column('Q:Q', 30)
          sheet.set_column('R:R', 30)
          sheet.set_column('S:S', 30)
          sheet.set_column('T:T', 30)
          sheet.set_column('U:U', 30)
          sheet.set_column('V:V', 30)
          sheet.set_column('W:W', 30)
          sheet.set_column('X:X', 30)

          # sheet.merge_range('A1:Z1', "")
          # sheet.merge_range('A2:Z2', "")
          
          sheet.merge_range('A4:A5', "", title)
          sheet.merge_range('B4:B5', "", title)
          sheet.merge_range('C4:C5', "", title)
          sheet.merge_range('D4:D5', "", title)

          sheet.merge_range('E4:K4', "", title)
          sheet.merge_range('L4:L5', "", title)
          sheet.merge_range('M4:M5', "", title)
          sheet.merge_range('N4:U4', "", title)

          sheet.merge_range('V4:V5', "", title)
          sheet.merge_range('W4:W5', "", title)
          sheet.merge_range('X4:X5', "", title)


          sheet.write('A1', 'PT.SUNTECH PLASTICS INDUSTRIES BATAM', title_parent)
          sheet.write('A2', 'Shortage Material Report' + ' ' + date.strftime('%d-%m-%Y') + ' to ' + date_end.strftime('%d-%m-%Y'), title_parent)

          sheet.write('A4', 'Part Number', title)
          sheet.write('B4', 'Category', title)
          sheet.write('C4', 'Description', title)
          sheet.write('D4', 'UoM', title)
          sheet.write('E4', 'After Deduct Plastic Part Stock', title)
          sheet.write('L4', 'Stock Qty', title)
          sheet.write('M4', 'Outstanding PO', title)
          sheet.write('N4', ' After Deduct plastic part stock + Resin MB Needle stock and Resin MB Needle PO Balance', title)
          sheet.write('V4', 'Total Requirement based on PO A/f deduct part stock', title)
          sheet.write('W4', 'Total Shortage Based on PO', title)
          sheet.write('X4', 'Remarks', title)

          sheet.write('E5', 'Requirement JIT' + date_end.strftime("%B"), title)
          sheet.write('F5', 'Requirement JIT' + date_one_format.strftime("%b"), title)
          sheet.write('G5', 'Requirement FC' + date_two_format.strftime("%b"), title)
          sheet.write('H5', 'Requirement FC' + date_three_format.strftime("%b"), title)
          sheet.write('I5', 'Requirement FC' + date_four_format.strftime("%b"), title)
          sheet.write('J5', 'Requirement FC' + date_five_format.strftime("%b"), title)
          sheet.write('K5', 'Requirement FC' + date_six_format.strftime("%b"), title)
          sheet.write('N5', 'Shortage JIT Current Month', title)
          sheet.write('O5', 'Shortage JIT' + date_one_format.strftime("%b"), title)
          sheet.write('P5', 'Shortage FC' + date_two_format.strftime("%b"), title)
          sheet.write('Q5', 'Shortage FC' + date_three_format.strftime("%b"), title)
          sheet.write('R5', 'Shortage FC' + date_four_format.strftime("%b"), title)
          sheet.write('S5', 'Shortage FC' + date_five_format.strftime("%b"), title)
          sheet.write('T5', 'Shortage FC' + date_six_format.strftime("%b"), title)
          sheet.write('U5', 'Total Shortage Based on M2 JIT & M5 FC ', title)

          row = 5
          index = 0
          jit_one = 0
          jit_two = 0
          jit_two = 0
          fc_one = 0
          fc_two = 0
          fc_three = 0
          fc_four = 0
          fc_five = 0
          total_po = 0
          total_shortage = 0 
          for boms in component:
              index += 1
              if index != len(component):
                  if boms.product_id.id != component[index-2].product_id.id:
                      jit_one = 0
                      jit_two = 0
                      jit_two = 0
                      fc_one = 0
                      fc_two = 0
                      fc_three = 0
                      fc_four = 0
                      fc_five = 0
                      total_po = 0   
                      total_shortage = 0
                  if boms.product_id.id == component[index].product_id.id:
                      if boms.bom_id.product_id.active == True:
                          if boms.optional_id.sequences == 1 or boms.component_type_secondary == 'metal':
                              if boms.bom_id.product_id.is_rawpart == True:

                                  # get stock item in
                                  stock_fg_in_ids = stock_move_obj.search([('product_id.default_code','=', boms.bom_id.product_id.code_part), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_in_fg = sum(stock_fg_in_ids.mapped('qty_done'))

                                  # get stock item out
                                  stock_fg_out_ids = stock_move_obj.search([('product_id.default_code','=', boms.bom_id.product_id.code_part), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_out_fg = sum(stock_fg_out_ids.mapped('qty_done'))

                                  # get stock item in rawpart
                                  stock_fg_in_rawpart_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_in_rawpart_fg = sum(stock_fg_in_rawpart_ids.mapped('qty_done'))

                                  # get stock item out rawpart
                                  stock_fg_out_rawpart_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_out_rawpart_fg = sum(stock_fg_out_rawpart_ids.mapped('qty_done'))

                                  # get stock item Machine
                                  quantity_machine_obj = self.env['product.product'].search([('default_code', '=', boms.bom_id.product_id.code_part)])
                                  quantity_machine = sum(quantity_machine_obj.mapped('quantity_machine'))

                                  # get stock on hand rawpart
                                  stock_onhand_ids = self.env['stock.quant'].search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88)])
                                  stock_onhand = sum(stock_onhand_ids.mapped('quantity'))

                                  # get stock on hand rawpart
                                  stock_onhand_rawpart_ids = self.env['stock.quant'].search([('product_id.default_code','=', boms.bom_id.product_id.code_part), ('location_id', '=', 88)])
                                  stock_onhand_rawpart = sum(stock_onhand_rawpart_ids.mapped('quantity'))     

                                  # get stock item
                                  date_now = datetime.today()
                                  if doc.date_end >= date_now.date():
                                      stock_fg = stock_onhand + stock_onhand_rawpart + quantity_machine + boms.bom_id.product_id.quantity_machine
                                  else:
                                      stock_fg = (stock_in_fg - stock_out_fg) + (stock_in_rawpart_fg - stock_out_rawpart_fg) + quantity_machine + boms.bom_id.product_id.quantity_machine

                                  # get delivery
                                  move_ids_without_package = picking_ids.mapped('move_ids_without_package')
                                  pick_obj = move_ids_without_package.filtered(lambda r: r.picking_id.scheduled_date >= jit_start_date and r.picking_id.scheduled_date < jit_end_date_use and r.product_id.default_code == boms.bom_id.product_id.code_part and r.state == 'done')
                                  delivery = sum(pick_obj.mapped('quantity_done'))
                                  
                                  # get jit data
                                  jit_end_date_one = bso_start_date + relativedelta(months=1)
                                  blanket_ids = bso_ids.mapped('blanket_ids')
                                  jit_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= bso_start_date.date() and r.order_id.contract_start < jit_end_date_one.date() and r.product_id.default_code == boms.bom_id.product_id.code_part)                            
                                  if boms.component_type == 'resin':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.unit_weight) / 1000 < 0:
                                          jit_one += (jit_one_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000                                            
                                      if (resin_one * boms.quantity_mb) / 100 < 0:
                                          jit_one += (resin_one * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.quantity_needle) < 0:
                                          jit_one += (jit_one_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_one / boms.quantity_pigment) < 0:
                                          jit_one += (resin_one / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.quantity_metal) < 0:
                                          jit_one += (jit_one_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.product_secc_qty) < 0:
                                          jit_one += (jit_one_datas * boms.product_secc_qty)

                                  jit_end_date_two = jit_end_date_one + relativedelta(months=1)
                                  blanket_ids = bso_ids.mapped('blanket_ids')
                                  jit_bso_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_one.date() and r.order_id.contract_start < jit_end_date_two.date() and r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.unit_weight) / 1000 < 0:
                                          jit_two += (jit_two_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_two * boms.quantity_mb) / 100 < 0:
                                          jit_two += (resin_two * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.quantity_needle) < 0:
                                          jit_two += (jit_two_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_two / boms.quantity_pigment) < 0:
                                          jit_two += (resin_two / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.quantity_metal) < 0:
                                          jit_two += (jit_two_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.product_secc_qty) < 0:
                                          jit_two += (jit_two_datas * boms.product_secc_qty)

                                  # get fc data
                                  fc_end_date_one = jit_end_date_two.date() + relativedelta(months=1)                                
                                  blanket_ids = bso_ids.mapped('blanket_ids')
                                  fc_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_two.date() and r.order_id.contract_start < fc_end_date_one and r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.unit_weight) / 1000 < 0:
                                          fc_one += (fc_one_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_three * boms.quantity_mb) / 100 < 0:
                                          fc_one += (resin_three * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.quantity_needle) < 0:
                                          fc_one += (fc_one_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_three / boms.quantity_pigment) < 0:
                                          fc_one += (resin_three / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.quantity_metal) < 0:
                                          fc_one += (fc_one_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.product_secc_qty) < 0:
                                          fc_one += (fc_one_datas * boms.product_secc_qty)

                                  fc_end_date_two = fc_end_date_one + relativedelta(months=1)
                                  fc_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_one and r.order_id.contract_start < fc_end_date_two and r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.unit_weight) / 1000 < 0:
                                          fc_two += (fc_two_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_four * boms.quantity_mb) / 100 < 0:
                                          fc_two += (resin_four * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.quantity_needle) < 0:
                                          fc_two += (fc_two_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_four / boms.quantity_pigment) < 0:
                                          fc_two += (resin_four / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.quantity_metal) < 0:
                                          fc_two += (fc_two_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.product_secc_qty) < 0:
                                          fc_two += (fc_two_datas * boms.product_secc_qty)
                                  
                                  fc_end_date_three = fc_end_date_two + relativedelta(months=1)
                                  fc_three_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_two and r.order_id.contract_start < fc_end_date_three and r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.unit_weight) / 1000 < 0:
                                          fc_three += (fc_three_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                                      if (resin_five * boms.quantity_mb) / 100 < 0:
                                          fc_three += (resin_five * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.quantity_needle) < 0:
                                          fc_three += (fc_three_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                                      if (resin_five / boms.quantity_pigment) < 0:
                                          fc_three += (resin_five / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.quantity_metal) < 0:
                                          fc_three += (fc_three_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.product_secc_qty) < 0:
                                          fc_three += (fc_three_datas * boms.product_secc_qty)

                                  fc_end_date_four = fc_end_date_three + relativedelta(months=1)
                                  fc_four_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_three and r.order_id.contract_start < fc_end_date_four and r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.unit_weight) / 1000 < 0:
                                          fc_four += (fc_four_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                                      if (resin_six * boms.quantity_mb) / 100 < 0:
                                          fc_four += (resin_six * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.quantity_needle) < 0:
                                          fc_four += (fc_four_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                                      if (resin_six / boms.quantity_pigment) < 0:
                                          fc_four += (resin_six / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.quantity_metal) < 0:
                                          fc_four += (fc_four_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.product_secc_qty) < 0:
                                          fc_four += (fc_four_datas * boms.product_secc_qty)

                                  fc_end_date_five = fc_end_date_four + relativedelta(months=1)
                                  fc_five_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_four and r.order_id.contract_start < fc_end_date_five and r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.unit_weight) / 1000 < 0:
                                          fc_five += (fc_five_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                                      if (resin_seven * boms.quantity_mb) / 100 < 0:
                                          fc_five += (resin_seven * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.quantity_needle) < 0:
                                          fc_five += (fc_five_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                                      if (resin_seven / boms.quantity_pigment) < 0:
                                          fc_five += (resin_seven / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.quantity_metal) < 0:
                                          fc_five += (fc_five_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.product_secc_qty) < 0:
                                          fc_five += (fc_five_datas * boms.product_secc_qty)
                                  
                                  # get po
                                  order_line = sale_ids.mapped('order_line')
                                  so_obj = order_line.filtered(lambda r: r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                                      total_po += (resin_eight * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_needle) 
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                                      total_po += (resin_eight / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_metal) 
                                  elif boms.component_type_secondary == 'metal':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.product_secc_qty)                            

                                  # get total shortage
                                  order_line = sale_ids.mapped('order_line')
                                  so_obj = order_line.filtered(lambda r: r.product_id.default_code == boms.bom_id.product_id.code_part)
                                  if boms.component_type == 'resin':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.unit_weight) / 1000 < 0:
                                          total_shortage += (overall * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      resin_eight = (overall * resin_obj.unit_weight) / 1000
                                      if (resin_eight * boms.quantity_mb) / 100 < 0:
                                          total_shortage += (resin_eight * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.quantity_needle) < 0:
                                          total_shortage += (overall * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      resin_eight = (overall * resin_obj.unit_weight) / 1000
                                      if (resin_eight / boms.quantity_pigment) < 0:
                                          total_shortage += (resin_eight / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.quantity_metal) < 0:
                                          total_shortage += (overall * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.product_secc_qty) < 0:
                                          total_shortage += (overall * boms.product_secc_qty)
                              else:
                                  # get stock item in
                                  stock_fg_in_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_in_fg = sum(stock_fg_in_ids.mapped('qty_done'))

                                  # get stock item out
                                  stock_fg_out_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_out_fg = sum(stock_fg_out_ids.mapped('qty_done'))

                                  # get stock item rawpart in
                                  stock_fg_in_ids = stock_move_obj.search([('product_id.code_part','=', boms.bom_id.product_id.default_code), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_in_raw_fg = sum(stock_fg_in_ids.mapped('qty_done'))

                                  # get stock item rawpart out
                                  stock_fg_out_ids = stock_move_obj.search([('product_id.code_part','=', boms.bom_id.product_id.default_code), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                                  stock_out_raw_fg = sum(stock_fg_out_ids.mapped('qty_done'))

                                  # get stock on hand
                                  stock_onhand_ids = self.env['stock.quant'].search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88)])
                                  stock_onhand = sum(stock_onhand_ids.mapped('quantity'))

                                  # get stock on hand
                                  stock_onhand_raw_ids = self.env['stock.quant'].search([('product_id.code_part','=', boms.bom_id.product_id.default_code), ('location_id', '=', 88)])
                                  stock_onhand_raw = sum(stock_onhand_raw_ids.mapped('quantity'))

                                  # get stock item Machine
                                  quantity_machine_obj = self.env['product.product'].search([('code_part', '=', boms.bom_id.product_id.default_code)])
                                  quantity_machine = sum(quantity_machine_obj.mapped('quantity_machine'))

                                  # get stock item
                                  date_now = datetime.today()
                                  if doc.date_end >= date_now.date():
                                      stock_fg = stock_onhand + boms.bom_id.product_id.quantity_machine + stock_onhand_raw + quantity_machine
                                  else:
                                      stock_fg = (stock_in_raw_fg - stock_out_raw_fg) + (stock_in_fg - stock_out_fg) + boms.bom_id.product_id.quantity_machine + quantity_machine

                                  # get delivery
                                  move_ids_without_package = picking_ids.mapped('move_ids_without_package')
                                  pick_obj = move_ids_without_package.filtered(lambda r: r.picking_id.scheduled_date >= jit_start_date and r.picking_id.scheduled_date < jit_end_date_use and r.product_id.id == boms.bom_id.product_id.id and r.state == 'done')
                                  delivery = sum(pick_obj.mapped('quantity_done'))
                                  
                                  # get jit data
                                  jit_end_date_one = bso_start_date + relativedelta(months=1)
                                  blanket_ids = bso_ids.mapped('blanket_ids')
                                  jit_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= bso_start_date.date() and r.order_id.contract_start < jit_end_date_one.date() and r.product_id.id == boms.bom_id.product_id.id)                            
                                  if boms.component_type == 'resin':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.unit_weight) / 1000 < 0:
                                          jit_one += (jit_one_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_one * boms.quantity_mb) / 100 < 0:
                                          jit_one += (resin_one * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.quantity_needle) < 0:
                                          jit_one += (jit_one_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigmet':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_one / boms.quantity_pigmet) < 0:
                                          jit_one += (resin_one / boms.quantity_pigmet)
                                  elif boms.component_type == 'metal':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.quantity_metal) < 0:
                                          jit_one += (jit_one_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                                      jit_one_datas = stock_fg - (jit_one_data - delivery)
                                      if (jit_one_datas * boms.product_secc_qty) < 0:
                                          jit_one += (jit_one_datas * boms.product_secc_qty)

                                  jit_end_date_two = jit_end_date_one + relativedelta(months=1)
                                  blanket_ids = bso_ids.mapped('blanket_ids')
                                  jit_bso_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_one.date() and r.order_id.contract_start < jit_end_date_two.date() and r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.unit_weight) / 1000 < 0:
                                          jit_two += (jit_two_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_two * boms.quantity_mb) / 100 < 0:
                                          jit_two += (resin_two * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.quantity_needle) < 0:
                                          jit_two += (jit_two_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_two / boms.quantity_pigment) < 0:
                                          jit_two += (resin_two / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.quantity_metal) < 0:
                                          jit_two += (jit_two_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                                      jit_two_datas = jit_one_datas - jit_two_data
                                      if (jit_two_datas * boms.product_secc_qty) < 0:
                                          jit_two += (jit_two_datas * boms.product_secc_qty)

                                  # get fc data
                                  fc_end_date_one = jit_end_date_two.date() + relativedelta(months=1)                                
                                  blanket_ids = bso_ids.mapped('blanket_ids')
                                  fc_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_two.date() and r.order_id.contract_start < fc_end_date_one and r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.unit_weight) / 1000 < 0:
                                          fc_one += (fc_one_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_three * boms.quantity_mb) / 100 < 0:
                                          fc_one += (resin_three * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.quantity_needle) < 0:
                                          fc_one += (fc_one_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                                      if (resin_three / boms.quantity_pigment) < 0:
                                          fc_one += (resin_three / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.quantity_metal) < 0:
                                          fc_one += (fc_one_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                                      fc_one_datas = jit_two_datas - fc_one_data
                                      if (fc_one_datas * boms.product_secc_qty) < 0:
                                          fc_one += (fc_one_datas * boms.product_secc_qty)

                                  fc_end_date_two = fc_end_date_one + relativedelta(months=1)
                                  fc_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_one and r.order_id.contract_start < fc_end_date_two and r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.unit_weight) / 1000 < 0:
                                          fc_two += (fc_two_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_four * boms.quantity_mb) / 100 < 0:
                                          fc_two += (resin_four * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.quantity_needle) < 0:
                                          fc_two += (fc_two_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                                      if (resin_four / boms.quantity_pigment) < 0:
                                          fc_two += (resin_four / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.quantity_metal) < 0:
                                          fc_two += (fc_two_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                                      fc_two_datas = fc_one_datas - fc_two_data
                                      if (fc_two_datas * boms.product_secc_qty) < 0:
                                          fc_two += (fc_two_datas * boms.product_secc_qty)
                                  
                                  fc_end_date_three = fc_end_date_two + relativedelta(months=1)
                                  fc_three_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_two and r.order_id.contract_start < fc_end_date_three and r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.unit_weight) / 1000 < 0:
                                          fc_three += (fc_three_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                                      if (resin_five * boms.quantity_mb) / 100 < 0:
                                          fc_three += (resin_five * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.quantity_needle) < 0:
                                          fc_three += (fc_three_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                                      if (resin_five / boms.quantity_pigment) < 0:
                                          fc_three += (resin_five / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.quantity_metal) < 0:
                                          fc_three += (fc_three_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                                      fc_three_datas = fc_two_datas - fc_three_data
                                      if (fc_three_datas * boms.product_secc_qty) < 0:
                                          fc_three += (fc_three_datas * boms.product_secc_qty)

                                  fc_end_date_four = fc_end_date_three + relativedelta(months=1)
                                  fc_four_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_three and r.order_id.contract_start < fc_end_date_four and r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.unit_weight) / 1000 < 0:
                                          fc_four += (fc_four_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                                      if (resin_six * boms.quantity_mb) / 100 < 0:
                                          fc_four += (resin_six * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.quantity_needle) < 0:
                                          fc_four += (fc_four_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                                      if (resin_six / boms.quantity_pigment) < 0:
                                          fc_four += (resin_six / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.quantity_metal) < 0:
                                          fc_four += (fc_four_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                                      fc_four_datas = fc_three_datas - fc_four_data
                                      if (fc_four_datas * boms.product_secc_qty) < 0:
                                          fc_four += (fc_four_datas * boms.product_secc_qty)

                                  fc_end_date_five = fc_end_date_four + relativedelta(months=1)
                                  fc_five_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_four and r.order_id.contract_start < fc_end_date_five and r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.unit_weight) / 1000 < 0:
                                          fc_five += (fc_five_datas * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                                      if (resin_seven * boms.quantity_mb) / 100 < 0:
                                          fc_five += (resin_seven * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.quantity_needle) < 0:
                                          fc_five += (fc_five_datas * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                                      if (resin_seven / boms.quantity_pigment) < 0:
                                          fc_five += (resin_seven / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.quantity_metal) < 0:
                                          fc_five += (fc_five_datas * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                                      fc_five_datas = fc_four_datas - fc_five_data
                                      if (fc_five_datas * boms.product_secc_qty) < 0:
                                          fc_five += (fc_five_datas * boms.product_secc_qty)
                                  
                                  # get po
                                  order_line = sale_ids.mapped('order_line')
                                  so_obj = order_line.filtered(lambda r: r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                                      total_po += (resin_eight * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                                      total_po += (resin_eight / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_metal) 
                                  elif boms.component_type_secondary == 'metal':
                                      total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.product_secc_qty)                            

                                  # get total shortage
                                  order_line = sale_ids.mapped('order_line')
                                  so_obj = order_line.filtered(lambda r: r.product_id.id == boms.bom_id.product_id.id)
                                  if boms.component_type == 'resin':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.unit_weight) / 1000 < 0:
                                          total_shortage += (overall * boms.unit_weight) / 1000
                                  elif boms.component_type == 'mb':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      resin_eight = (overall * resin_obj.unit_weight) / 1000
                                      if (resin_eight * boms.quantity_mb) / 100 < 0:
                                          total_shortage += (resin_eight * boms.quantity_mb) / 100
                                  elif boms.component_type == 'needle':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.quantity_needle) < 0:
                                          total_shortage += (overall * boms.quantity_needle)
                                  elif boms.component_type == 'pigment':
                                      resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      resin_eight = (overall * resin_obj.unit_weight) / 1000
                                      if (resin_eight / boms.quantity_pigment) < 0:
                                          total_shortage += (resin_eight / boms.quantity_pigment)
                                  elif boms.component_type == 'metal':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.quantity_metal) < 0:
                                          total_shortage += (overall * boms.quantity_metal)
                                  elif boms.component_type_secondary == 'metal':
                                      po_total = sum(so_obj.mapped('product_uom_qty'))
                                      do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                                      po_balance = po_total - do_total
                                      overall = stock_fg - po_balance
                                      if (overall * boms.product_secc_qty) < 0:
                                          total_shortage += (overall * boms.product_secc_qty)

                          # get ppo
                          order_line = purchase_ids.mapped('order_line')
                          po_obj = order_line.filtered(lambda r: r.product_id.id == boms.product_id.id and r.order_id.date_order <= jit_end_date_use)
                          total_ppo = (sum(po_obj.mapped('product_qty'))) - (sum(po_obj.mapped('qty_received')))

                          # get stock item in
                          stock_in_ids = stock_move_obj.search([('product_id','=', int(boms.product_id.id)), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_in = sum(stock_in_ids.mapped('qty_done'))

                          # get stock item out
                          stock_out_ids = stock_move_obj.search([('product_id','=', int(boms.product_id.id)), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_out = sum(stock_out_ids.mapped('qty_done'))

                          # get stock item
                          stock = (stock_in - stock_out) + boms.product_id.quantity_machine
                                                      
                      continue                
                          
              if boms.bom_id.product_id.active == True:
                  if boms.optional_id.sequences == 1 or boms.component_type_secondary == 'metal':
                      if boms.bom_id.product_id.is_rawpart == True:
                          # get stock item in
                          stock_fg_in_ids = stock_move_obj.search([('product_id.default_code','=', boms.bom_id.product_id.code_part), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_in_fg = sum(stock_fg_in_ids.mapped('qty_done'))

                          # get stock item out
                          stock_fg_out_ids = stock_move_obj.search([('product_id.default_code','=', boms.bom_id.product_id.code_part), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_out_fg = sum(stock_fg_out_ids.mapped('qty_done'))

                          # get stock item in rawpart
                          stock_fg_in_rawpart_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_in_rawpart_fg = sum(stock_fg_in_rawpart_ids.mapped('qty_done'))

                          # get stock item out rawpart
                          stock_fg_out_rawpart_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_out_rawpart_fg = sum(stock_fg_out_rawpart_ids.mapped('qty_done'))

                          # get stock item Machine
                          quantity_machine_obj = self.env['product.product'].search([('default_code', '=', boms.bom_id.product_id.code_part)])
                          quantity_machine = sum(quantity_machine_obj.mapped('quantity_machine'))

                          # get stock on hand rawpart
                          stock_onhand_ids = self.env['stock.quant'].search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88)])
                          stock_onhand = sum(stock_onhand_ids.mapped('quantity'))

                          # get stock on hand rawpart
                          stock_onhand_rawpart_ids = self.env['stock.quant'].search([('product_id.default_code','=', boms.bom_id.product_id.code_part), ('location_id', '=', 88)])
                          stock_onhand_rawpart = sum(stock_onhand_rawpart_ids.mapped('quantity'))     

                          # get stock item
                          date_now = datetime.today()
                          if doc.date_end >= date_now.date():
                              stock_fg = stock_onhand + stock_onhand_rawpart + quantity_machine + boms.bom_id.product_id.quantity_machine
                          else:
                              stock_fg = (stock_in_fg - stock_out_fg) + (stock_in_rawpart_fg - stock_out_rawpart_fg) + quantity_machine

                          # get delivery
                          move_ids_without_package = picking_ids.mapped('move_ids_without_package')
                          pick_obj = move_ids_without_package.filtered(lambda r: r.picking_id.scheduled_date >= jit_start_date and r.picking_id.scheduled_date < jit_end_date_use and r.product_id.default_code == boms.bom_id.product_id.code_part and r.state == 'done')
                          delivery = sum(pick_obj.mapped('quantity_done'))
                          
                          # get jit data
                          jit_end_date_one = bso_start_date + relativedelta(months=1)
                          blanket_ids = bso_ids.mapped('blanket_ids')
                          jit_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= bso_start_date.date() and r.order_id.contract_start < jit_end_date_one.date() and r.product_id.default_code == boms.bom_id.product_id.code_part)                            
                          if boms.component_type == 'resin':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.unit_weight) / 1000 < 0:
                                  jit_one += (jit_one_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_one * boms.quantity_mb) / 100 < 0:
                                  jit_one += (resin_one * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.quantity_needle) < 0:
                                  jit_one += (jit_one_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_one / boms.quantity_pigment) < 0:
                                  jit_one += (resin_one / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.quantity_metal) < 0:
                                  jit_one += (jit_one_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.product_secc_qty) < 0:
                                  jit_one += (jit_one_datas * boms.product_secc_qty)

                          jit_end_date_two = jit_end_date_one + relativedelta(months=1)
                          blanket_ids = bso_ids.mapped('blanket_ids')
                          jit_bso_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_one.date() and r.order_id.contract_start < jit_end_date_two.date() and r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.unit_weight) / 1000 < 0:
                                  jit_two += (jit_two_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_two * boms.quantity_mb) / 100 < 0:
                                  jit_two += (resin_two * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.quantity_needle) < 0:
                                  jit_two += (jit_two_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_two / boms.quantity_pigment) < 0:
                                  jit_two += (resin_two / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.quantity_metal) < 0:
                                  jit_two += (jit_two_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.product_secc_qty) < 0:
                                  jit_two += (jit_two_datas * boms.product_secc_qty)

                          # get fc data
                          fc_end_date_one = jit_end_date_two.date() + relativedelta(months=1)                                
                          blanket_ids = bso_ids.mapped('blanket_ids')
                          fc_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_two.date() and r.order_id.contract_start < fc_end_date_one and r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.unit_weight) / 1000 < 0:
                                  fc_one += (fc_one_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_three * boms.quantity_mb) / 100 < 0:
                                  fc_one += (resin_three * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.quantity_needle) < 0:
                                  fc_one += (fc_one_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_three / boms.quantity_pigment) < 0:
                                  fc_one += (resin_three / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.quantity_metal) < 0:
                                  fc_one += (fc_one_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.product_secc_qty) < 0:
                                  fc_one += (fc_one_datas * boms.product_secc_qty)

                          fc_end_date_two = fc_end_date_one + relativedelta(months=1)
                          fc_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_one and r.order_id.contract_start < fc_end_date_two and r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.unit_weight) / 1000 < 0:
                                  fc_two += (fc_two_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_four * boms.quantity_mb) / 100 < 0:
                                  fc_two += (resin_four * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.quantity_needle) < 0:
                                  fc_two += (fc_two_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_four / boms.quantity_pigment) < 0:
                                  fc_two += (resin_four / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.quantity_metal) < 0:
                                  fc_two += (fc_two_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.product_secc_qty) < 0:
                                  fc_two += (fc_two_datas * boms.product_secc_qty)
                          
                          fc_end_date_three = fc_end_date_two + relativedelta(months=1)
                          fc_three_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_two and r.order_id.contract_start < fc_end_date_three and r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.unit_weight) / 1000 < 0:
                                  fc_three += (fc_three_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                              if (resin_five * boms.quantity_mb) / 100 < 0:
                                  fc_three += (resin_five * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.quantity_needle) < 0:
                                  fc_three += (fc_three_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                              if (resin_five / boms.quantity_pigment) < 0:
                                  fc_three += (resin_five / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.quantity_metal) < 0:
                                  fc_three += (fc_three_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.product_secc_qty) < 0:
                                  fc_three += (fc_three_datas * boms.product_secc_qty)

                          fc_end_date_four = fc_end_date_three + relativedelta(months=1)
                          fc_four_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_three and r.order_id.contract_start < fc_end_date_four and r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.unit_weight) / 1000 < 0:
                                  fc_four += (fc_four_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                              if (resin_six * boms.quantity_mb) / 100 < 0:
                                  fc_four += (resin_six * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.quantity_needle) < 0:
                                  fc_four += (fc_four_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                              if (resin_six / boms.quantity_pigment) < 0:
                                  fc_four += (resin_six / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.quantity_metal) < 0:
                                  fc_four += (fc_four_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.product_secc_qty) < 0:
                                  fc_four += (fc_four_datas * boms.product_secc_qty)

                          fc_end_date_five = fc_end_date_four + relativedelta(months=1)
                          fc_five_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_four and r.order_id.contract_start < fc_end_date_five and r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.unit_weight) / 1000 < 0:
                                  fc_five += (fc_five_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                              if (resin_seven * boms.quantity_mb) / 100 < 0:
                                  fc_five += (resin_seven * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.quantity_needle) < 0:
                                  fc_five += (fc_five_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                              if (resin_seven / boms.quantity_pigment) < 0:
                                  fc_five += (resin_seven / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.quantity_metal) < 0:
                                  fc_five += (fc_five_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.product_secc_qty) < 0:
                                  fc_five += (fc_five_datas * boms.product_secc_qty)
                          
                          # get po
                          order_line = sale_ids.mapped('order_line')
                          so_obj = order_line.filtered(lambda r: r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                              total_po += (resin_eight * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_needle) 
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                              total_po += (resin_eight / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_metal) 
                          elif boms.component_type_secondary == 'metal':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.product_secc_qty)                            

                          # get total shortage
                          order_line = sale_ids.mapped('order_line')
                          so_obj = order_line.filtered(lambda r: r.product_id.default_code == boms.bom_id.product_id.code_part)
                          if boms.component_type == 'resin':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.unit_weight) / 1000 < 0:
                                  total_shortage += (overall * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              resin_eight = (overall * resin_obj.unit_weight) / 1000
                              if (resin_eight * boms.quantity_mb) / 100 < 0:
                                  total_shortage += (resin_eight * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.quantity_needle) < 0:
                                  total_shortage += (overall * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              resin_eight = (overall * resin_obj.unit_weight) / 1000
                              if (resin_eight / boms.quantity_pigment) < 0:
                                  total_shortage += (resin_eight / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.quantity_metal) < 0:
                                  total_shortage += (overall * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.product_secc_qty) < 0:
                                  total_shortage += (overall * boms.product_secc_qty)
                      else:
                          # get stock item in
                          stock_fg_in_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_in_fg = sum(stock_fg_in_ids.mapped('qty_done'))

                          # get stock item out
                          stock_fg_out_ids = stock_move_obj.search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_out_fg = sum(stock_fg_out_ids.mapped('qty_done'))

                          # get stock item rawpart in
                          stock_fg_in_ids = stock_move_obj.search([('product_id.code_part','=', boms.bom_id.product_id.default_code), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_in_raw_fg = sum(stock_fg_in_ids.mapped('qty_done'))

                          # get stock item rawpart out
                          stock_fg_out_ids = stock_move_obj.search([('product_id.code_part','=', boms.bom_id.product_id.default_code), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                          stock_out_raw_fg = sum(stock_fg_out_ids.mapped('qty_done'))

                          # get stock on hand
                          stock_onhand_ids = self.env['stock.quant'].search([('product_id','=', boms.bom_id.product_id.id), ('location_id', '=', 88)])
                          stock_onhand = sum(stock_onhand_ids.mapped('quantity'))

                          # get stock on hand
                          stock_onhand_raw_ids = self.env['stock.quant'].search([('product_id.code_part','=', boms.bom_id.product_id.default_code), ('location_id', '=', 88)])
                          stock_onhand_raw = sum(stock_onhand_raw_ids.mapped('quantity'))

                          # get stock item Machine
                          quantity_machine_obj = self.env['product.product'].search([('code_part', '=', boms.bom_id.product_id.default_code)])
                          quantity_machine = sum(quantity_machine_obj.mapped('quantity_machine'))

                          # get stock item
                          date_now = datetime.today()
                          if doc.date_end >= date_now.date():
                              stock_fg = stock_onhand + boms.bom_id.product_id.quantity_machine + stock_onhand_raw + quantity_machine
                          else:
                              stock_fg = (stock_in_raw_fg - stock_out_raw_fg) + (stock_in_fg - stock_out_fg) + boms.bom_id.product_id.quantity_machine + quantity_machine
                          # get delivery
                          move_ids_without_package = picking_ids.mapped('move_ids_without_package')
                          pick_obj = move_ids_without_package.filtered(lambda r: r.picking_id.scheduled_date >= jit_start_date and r.picking_id.scheduled_date < jit_end_date_use and r.product_id.id == boms.bom_id.product_id.id and r.state == 'done')
                          delivery = sum(pick_obj.mapped('quantity_done'))
                          
                          # get jit data
                          jit_end_date_one = bso_start_date + relativedelta(months=1)
                          blanket_ids = bso_ids.mapped('blanket_ids')
                          jit_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= bso_start_date.date() and r.order_id.contract_start < jit_end_date_one.date() and r.product_id.id == boms.bom_id.product_id.id)                            
                          if boms.component_type == 'resin':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.unit_weight) / 1000 < 0:
                                  jit_one += (jit_one_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_one * boms.quantity_mb) / 100 < 0:
                                  jit_one += (resin_one * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.quantity_needle) < 0:
                                  jit_one += (jit_one_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigmet':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              resin_one = (jit_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_one / boms.quantity_pigmet) < 0:
                                  jit_one += (resin_one / boms.quantity_pigmet)
                          elif boms.component_type == 'metal':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.quantity_metal) < 0:
                                  jit_one += (jit_one_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              jit_one_data = sum(jit_one_obj.mapped('product_uom_qty')) 
                              jit_one_datas = stock_fg - (jit_one_data - delivery)
                              if (jit_one_datas * boms.product_secc_qty) < 0:
                                  jit_one += (jit_one_datas * boms.product_secc_qty)

                          jit_end_date_two = jit_end_date_one + relativedelta(months=1)
                          blanket_ids = bso_ids.mapped('blanket_ids')
                          jit_bso_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_one.date() and r.order_id.contract_start < jit_end_date_two.date() and r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.unit_weight) / 1000 < 0:
                                  jit_two += (jit_two_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_two * boms.quantity_mb) / 100 < 0:
                                  jit_two += (resin_two * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.quantity_needle) < 0:
                                  jit_two += (jit_two_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              resin_two = (jit_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_two / boms.quantity_pigment) < 0:
                                  jit_two += (resin_two / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.quantity_metal) < 0:
                                  jit_two += (jit_two_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              jit_two_data = sum(jit_bso_two_obj.mapped('product_uom_qty'))
                              jit_two_datas = jit_one_datas - jit_two_data
                              if (jit_two_datas * boms.product_secc_qty) < 0:
                                  jit_two += (jit_two_datas * boms.product_secc_qty)

                          # get fc data
                          fc_end_date_one = jit_end_date_two.date() + relativedelta(months=1)                                
                          blanket_ids = bso_ids.mapped('blanket_ids')
                          fc_one_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= jit_end_date_two.date() and r.order_id.contract_start < fc_end_date_one and r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.unit_weight) / 1000 < 0:
                                  fc_one += (fc_one_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_three * boms.quantity_mb) / 100 < 0:
                                  fc_one += (resin_three * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.quantity_needle) < 0:
                                  fc_one += (fc_one_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              resin_three = (fc_one_datas * resin_obj.unit_weight) / 1000
                              if (resin_three / boms.quantity_pigment) < 0:
                                  fc_one += (resin_three / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.quantity_metal) < 0:
                                  fc_one += (fc_one_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_one_data = sum(fc_one_obj.mapped('product_uom_qty')) 
                              fc_one_datas = jit_two_datas - fc_one_data
                              if (fc_one_datas * boms.product_secc_qty) < 0:
                                  fc_one += (fc_one_datas * boms.product_secc_qty)

                          fc_end_date_two = fc_end_date_one + relativedelta(months=1)
                          fc_two_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_one and r.order_id.contract_start < fc_end_date_two and r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.unit_weight) / 1000 < 0:
                                  fc_two += (fc_two_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_four * boms.quantity_mb) / 100 < 0:
                                  fc_two += (resin_four * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.quantity_needle) < 0:
                                  fc_two += (fc_two_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              resin_four = (fc_two_datas * resin_obj.unit_weight) / 1000
                              if (resin_four / boms.quantity_pigment) < 0:
                                  fc_two += (resin_four / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.quantity_metal) < 0:
                                  fc_two += (fc_two_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_two_data = sum(fc_two_obj.mapped('product_uom_qty')) 
                              fc_two_datas = fc_one_datas - fc_two_data
                              if (fc_two_datas * boms.product_secc_qty) < 0:
                                  fc_two += (fc_two_datas * boms.product_secc_qty)
                          
                          fc_end_date_three = fc_end_date_two + relativedelta(months=1)
                          fc_three_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_two and r.order_id.contract_start < fc_end_date_three and r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.unit_weight) / 1000 < 0:
                                  fc_three += (fc_three_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                              if (resin_five * boms.quantity_mb) / 100 < 0:
                                  fc_three += (resin_five * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.quantity_needle) < 0:
                                  fc_three += (fc_three_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              resin_five = (fc_three_datas * resin_obj.unit_weight) / 1000
                              if (resin_five / boms.quantity_pigment) < 0:
                                  fc_three += (resin_five / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.quantity_metal) < 0:
                                  fc_three += (fc_three_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_three_data = sum(fc_three_obj.mapped('product_uom_qty')) 
                              fc_three_datas = fc_two_datas - fc_three_data
                              if (fc_three_datas * boms.product_secc_qty) < 0:
                                  fc_three += (fc_three_datas * boms.product_secc_qty)

                          fc_end_date_four = fc_end_date_three + relativedelta(months=1)
                          fc_four_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_three and r.order_id.contract_start < fc_end_date_four and r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.unit_weight) / 1000 < 0:
                                  fc_four += (fc_four_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                              if (resin_six * boms.quantity_mb) / 100 < 0:
                                  fc_four += (resin_six * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.quantity_needle) < 0:
                                  fc_four += (fc_four_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              resin_six = (fc_four_datas * resin_obj.unit_weight) / 1000
                              if (resin_six / boms.quantity_pigment) < 0:
                                  fc_four += (resin_six / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.quantity_metal) < 0:
                                  fc_four += (fc_four_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_four_data = sum(fc_four_obj.mapped('product_uom_qty')) 
                              fc_four_datas = fc_three_datas - fc_four_data
                              if (fc_four_datas * boms.product_secc_qty) < 0:
                                  fc_four += (fc_four_datas * boms.product_secc_qty)

                          fc_end_date_five = fc_end_date_four + relativedelta(months=1)
                          fc_five_obj = blanket_ids.filtered(lambda r: r.order_id.contract_start >= fc_end_date_four and r.order_id.contract_start < fc_end_date_five and r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.unit_weight) / 1000 < 0:
                                  fc_five += (fc_five_datas * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                              if (resin_seven * boms.quantity_mb) / 100 < 0:
                                  fc_five += (resin_seven * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.quantity_needle) < 0:
                                  fc_five += (fc_five_datas * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              resin_seven = (fc_five_datas * resin_obj.unit_weight) / 1000
                              if (resin_seven / boms.quantity_pigment) < 0:
                                  fc_five += (resin_seven / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.quantity_metal) < 0:
                                  fc_five += (fc_five_datas * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              fc_five_data = sum(fc_five_obj.mapped('product_uom_qty')) 
                              fc_five_datas = fc_four_datas - fc_five_data
                              if (fc_five_datas * boms.product_secc_qty) < 0:
                                  fc_five += (fc_five_datas * boms.product_secc_qty)
                          
                          # get po
                          order_line = sale_ids.mapped('order_line')
                          so_obj = order_line.filtered(lambda r: r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                              total_po += (resin_eight * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              resin_eight = (sum(so_obj.mapped('product_uom_qty')) * resin_obj.unit_weight) / 1000
                              total_po += (resin_eight / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.quantity_metal) 
                          elif boms.component_type_secondary == 'metal':
                              total_po += (sum(so_obj.mapped('product_uom_qty')) * boms.product_secc_qty)                            

                          # get total shortage
                          order_line = sale_ids.mapped('order_line')
                          so_obj = order_line.filtered(lambda r: r.product_id.id == boms.bom_id.product_id.id)
                          if boms.component_type == 'resin':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.unit_weight) / 1000 < 0:
                                  total_shortage += (overall * boms.unit_weight) / 1000
                          elif boms.component_type == 'mb':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              resin_eight = (overall * resin_obj.unit_weight) / 1000
                              if (resin_eight * boms.quantity_mb) / 100 < 0:
                                  total_shortage += (resin_eight * boms.quantity_mb) / 100
                          elif boms.component_type == 'needle':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.quantity_needle) < 0:
                                  total_shortage += (overall * boms.quantity_needle)
                          elif boms.component_type == 'pigment':
                              resin_obj = self.env['mrp.bom.line'].search([('bom_id', '=', boms.bom_id.id), ('component_type', '=', 'resin'), ('optional_id.sequences','=', 1)], limit=1)
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              resin_eight = (overall * resin_obj.unit_weight) / 1000
                              if (resin_eight / boms.quantity_pigment) < 0:
                                  total_shortage += (resin_eight / boms.quantity_pigment)
                          elif boms.component_type == 'metal':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.quantity_metal) < 0:
                                  total_shortage += (overall * boms.quantity_metal)
                          elif boms.component_type_secondary == 'metal':
                              po_total = sum(so_obj.mapped('product_uom_qty'))
                              do_total = sum(so_obj.mapped('delivery_line_ids.quantity_done'))
                              po_balance = po_total - do_total
                              overall = stock_fg - po_balance
                              if (overall * boms.product_secc_qty) < 0:
                                  total_shortage += (overall * boms.product_secc_qty)

                  # get ppo
                  order_line = purchase_ids.mapped('order_line')
                  po_obj = order_line.filtered(lambda r: r.product_id.id == boms.product_id.id and r.order_id.date_order <= jit_end_date_use)
                  total_ppo = (sum(po_obj.mapped('product_qty'))) - (sum(po_obj.mapped('qty_received')))

                  # get stock item in
                  stock_in_ids = stock_move_obj.search([('product_id','=', int(boms.product_id.id)), ('location_dest_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                  stock_in = sum(stock_in_ids.mapped('qty_done'))

                  # get stock item out
                  stock_out_ids = stock_move_obj.search([('product_id','=', int(boms.product_id.id)), ('location_id', '=', 88), ('state', '=', 'done'), ('date', '<=', jit_end_date_use)])
                  stock_out = sum(stock_out_ids.mapped('qty_done'))

                  # get stock item
                  stock = (stock_in - stock_out) + boms.product_id.quantity_machine    

              
              shortage_1 = total_ppo + stock + jit_one
              shortage_2 = total_ppo + stock + jit_two
              shortage_3 = total_ppo + stock + fc_one
              shortage_4 = total_ppo + stock + fc_two
              shortage_5 = total_ppo + stock + fc_three
              shortage_6 = total_ppo + stock + fc_four
              shortage_7 = total_ppo + stock + fc_five

              requirment_stock = total_ppo + stock + total_shortage

              types = False
              if boms.component_type == 'resin':
                  types = 'Resin'
              elif boms.component_type == 'mb':
                  types = 'Masterbatch'
              elif boms.component_type == 'needle':
                  types = 'Needle'
              elif boms.component_type == 'pigment':
                  types = 'Pigment'
              elif boms.component_type == 'metal':
                  types = 'Metal Part'  
              elif boms.component_type_secondary == 'metal':
                  types = 'Metal Part'

              if not boms.product_id.default_code:
                  sheet.write(row, 0 , '', table_center)
              else:
                  sheet.write(row, 0 , boms.product_id.default_code, table_center)
              sheet.write(row, 1 , types, table_center)
              if not boms.product_id.name:
                  sheet.write(row, 2 , '', table_center)
              else:
                  sheet.write(row, 2 , boms.product_id.name, table_center)
              if not boms.product_id.uom_id.name:
                  sheet.write(row, 3 , '', table_center)
              else:
                  sheet.write(row, 3 , boms.product_id.uom_id.name, table_center)                

              sheet.write(row, 4 , round(jit_one), table_center)
              sheet.write(row, 5 , round(jit_two), table_center)
              sheet.write(row, 6 , round(fc_one), table_center)
              sheet.write(row, 7 , round(fc_two), table_center)
              sheet.write(row, 8 , round(fc_three), table_center)
              sheet.write(row, 9 , round(fc_four), table_center)
              sheet.write(row, 10 , round(fc_five), table_center)
              sheet.write(row, 11 , stock, table_center)
              sheet.write(row, 12 , round(total_ppo), table_center)
              sheet.write(row, 13 , round(shortage_1), table_center)
              sheet.write(row, 14 , round(shortage_2), table_center)
              sheet.write(row, 15 , round(shortage_3), table_center)
              sheet.write(row, 16 , round(shortage_4), table_center)
              sheet.write(row, 17 , round(shortage_5), table_center)
              sheet.write(row, 18 , round(shortage_6), table_center)
              sheet.write(row, 19 , round(shortage_7), table_center)
              sheet.write(row, 20 , round(shortage_7), table_center)
              sheet.write(row, 21 , round(total_shortage), table_center)
              sheet.write(row, 22 , round(requirment_stock), table_center)
              if not boms.product_id.remarks:
                  sheet.write(row, 23 , '', table_center)
              else:
                  sheet.write(row, 23 , boms.product_id.remarks, table_center)

              row += 1
              jit_one = 0
              jit_two = 0
              fc_one = 0
              fc_two = 0
              fc_three = 0
              fc_four = 0
              fc_five = 0
              total_po = 0
              total_shortage = 0
