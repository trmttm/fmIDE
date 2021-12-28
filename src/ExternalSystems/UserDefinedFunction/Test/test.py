import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        from ....ExternalSystems.UserDefinedFunction import UDFBuilder
        self.udf_builder = UDFBuilder()

    def test_udf1(self):
        request_model = {'arguments': ('var_cash_bb_cash_bb', 'var_interest_rate_rate'),
                         'circular_dependencies': ('interest_income', 'cash_eb', 'base'),
                         'direct_links_mutable': (),
                         'folder_name': None,
                         'formulas': ('var_cash_eb_cash_eb = '
                                      'var_cash_bb_cash_bb+var_interest_income_interest',
                                      'var_base_base = (var_cash_bb_cash_bb+var_cash_eb_cash_eb)/2',
                                      'var_interest_income_interest = '
                                      'var_base_base*var_interest_rate_rate'),
                         'name': 'user_defined_function',
                         'max_loop': 10000,
                         'target_value': 'var_cash_eb_cash_eb',
                         'tolerance': 0.001,
                         'variables': ('var_base_base',
                                       'var_cash_bb_cash_bb',
                                       'var_cash_eb_cash_eb',
                                       'var_interest_income_interest',
                                       'var_interest_rate_rate'),
                         'minimum_iteration': 1}
        expectation = """Option Explicit

Dim max_loop
Dim tolerance
Dim iteration
Dim target_value

Dim previous_0_var_cash_eb_cash_eb 
Dim previous_1_var_base_base 
Dim previous_2_var_interest_income_interest 


Dim delta
Dim delta_0_var_cash_eb_cash_eb 
Dim delta_1_var_base_base 
Dim delta_2_var_interest_income_interest 

Dim var_base_base
Dim var_cash_bb_cash_bb
Dim var_cash_eb_cash_eb
Dim var_interest_income_interest
Dim var_interest_rate_rate

Function user_defined_function( _
var_cash_bb_cash_bb, var_interest_rate_rate) 
	max_loop = 10000
	tolerance = 0.001

	For iteration = 1 To max_loop

		' Values before calculation
		previous_0_var_cash_eb_cash_eb  = var_cash_eb_cash_eb 
		previous_1_var_base_base  = var_base_base 
		previous_2_var_interest_income_interest  = var_interest_income_interest 

		' Calculations
		var_cash_eb_cash_eb = var_cash_bb_cash_bb+var_interest_income_interest
		var_base_base = (var_cash_bb_cash_bb+var_cash_eb_cash_eb)/2
		var_interest_income_interest = var_base_base*var_interest_rate_rate


		' Compare values after calculations
		delta_0_var_cash_eb_cash_eb  = Abs(previous_0_var_cash_eb_cash_eb  - var_cash_eb_cash_eb )
		delta_1_var_base_base  = Abs(previous_1_var_base_base  - var_base_base )
		delta_2_var_interest_income_interest  = Abs(previous_2_var_interest_income_interest  - var_interest_income_interest )

		' Cumulative absolute differences (deltas)
		delta = 0
		delta = delta + delta_0_var_cash_eb_cash_eb 
		delta = delta + delta_1_var_base_base 
		delta = delta + delta_2_var_interest_income_interest 

		' If cumulative differences is smaller than tolerance, then exit function.
		If iteration > 1 And delta < tolerance Then
			target_value = var_cash_eb_cash_eb
			user_defined_function = var_cash_eb_cash_eb
			Exit Function
		End If
	Next iteration
End Function

Function Min(ParamArray values() As Variant) As Variant
   Dim minValue, Value As Variant
   minValue = values(0)
   For Each Value In values
       If Value < minValue Then minValue = Value
   Next
   Min = minValue
End Function

Function Max(ParamArray values() As Variant) As Variant
   Dim maxValue, Value As Variant
   maxValue = values(0)
   For Each Value In values
       If Value > maxValue Then maxValue = Value
   Next
   Max = maxValue
End Function
"""
        self.udf_builder.export(**request_model)
        self.assertEqual(self.udf_builder.text, expectation)

    def test_udf2(self):
        request_model = {'arguments': ('var_65_ebit',
                                       'var_67_delta_working_capital',
                                       'var_68_depreciation',
                                       'var_69_amortization',
                                       'var_116_ebit',
                                       'var_158_draw_down',
                                       'var_164_interest_payment',
                                       'var_166_avaialble_cash',
                                       'var_168_cfi',
                                       'var_171_cash_bb',
                                       'var_172_plug_interest_rate',
                                       'var_240_revolver_bb',
                                       'var_247_plug_interest_rate',
                                       'var_257_interest_expense',
                                       'var_269_repayment',
                                       'var_308_income_tax_rate'),
                         'direct_links_mutable': (('var_70_total_cfo', 'var_98_cash_flow_from_operation'),
                                                  ('var_139_total_interest_income', 'var_117_interest_income'),
                                                  ('var_138_total_interest_expense', 'var_118_interest_expense'),
                                                  ('var_165_remaining_cash', 'var_157_available_cash'),
                                                  ('var_98_cash_flow_from_operation', 'var_167_cfo'),
                                                  ('var_228_remaining_cash', 'var_219_cash_eb'),
                                                  ('var_156_remaining_cash', 'var_229_available_cash'),
                                                  ('var_230_revolver_dd', 'var_241_draw_down'),
                                                  ('var_231_revolver_repayment', 'var_242_repayment'),
                                                  ('var_323_cf_revolver_interest', 'var_290_revolver_interest'),
                                                  ('var_327_cf_interest_on_cash', 'var_292_cash_interest'),
                                                  ('var_119_ebt', 'var_309_taxable_income')),
                         'folder_name': None,
                         'formulas': ('var_66_tax_payment = var_215_cf_tax_payment+0',
                                      'var_70_total_cfo = '
                                      'var_65_ebit+var_66_tax_payment+var_67_delta_working_capital+var_69_amortization+var_68_depreciation',
                                      'var_119_ebt = var_116_ebit-var_118_interest_expense+var_117_interest_income',
                                      'var_138_total_interest_expense = '
                                      'var_257_interest_expense+var_253_revolver_interest',
                                      'var_139_total_interest_income = var_173_interest_on_cash+0',
                                      'var_156_remaining_cash = '
                                      'var_157_available_cash+var_158_draw_down+var_159_repayment+var_164_interest_payment+var_290_revolver_interest+var_292_cash_interest',
                                      'var_159_repayment = min(max(var_157_available_cash+var_158_draw_down, 0), '
                                      'var_269_repayment)*-1',
                                      'var_165_remaining_cash = var_166_avaialble_cash+var_167_cfo+var_168_cfi',
                                      'var_173_interest_on_cash = var_172_plug_interest_rate*var_218_base',
                                      'var_215_cf_tax_payment = -1*var_310_income_tax_expense',
                                      'var_218_base = (var_219_cash_eb+var_171_cash_bb)/2',
                                      'var_228_remaining_cash = '
                                      'var_229_available_cash+var_230_revolver_dd+var_231_revolver_repayment',
                                      'var_230_revolver_dd = -1*min(0, var_229_available_cash)',
                                      'var_231_revolver_repayment = -1*min(max(var_240_revolver_bb, 0), '
                                      'max(var_229_available_cash, 0))',
                                      'var_239_revolver = var_240_revolver_bb+var_241_draw_down+var_242_repayment',
                                      'var_253_revolver_interest = var_259_base*var_247_plug_interest_rate',
                                      'var_259_base = (var_240_revolver_bb+var_239_revolver)/2',
                                      'var_310_income_tax_expense = var_308_income_tax_rate*var_309_taxable_income',
                                      'var_323_cf_revolver_interest = var_253_revolver_interest*-1',
                                      'var_327_cf_interest_on_cash = var_173_interest_on_cash+0'),
                         'name': 'user_defined_function',
                         'max_loop': 10000,
                         'target_value': 'var_156_remaining_cash',
                         'tolerance': 0.001,
                         'variables': ('var_100_cash_flow_from_financing',
                                       'var_101_cash_bb',
                                       'var_107_revenue',
                                       'var_108_cost_of_goods',
                                       'var_10_other_cl',
                                       'var_110_sga',
                                       'var_111_other_expenses',
                                       'var_112_other_incomes',
                                       'var_114_depreciation',
                                       'var_115_amortization',
                                       'var_116_ebit',
                                       'var_117_interest_income',
                                       'var_118_interest_expense',
                                       'var_119_ebt',
                                       'var_11_plug__revolver',
                                       'var_120_tax',
                                       'var_138_total_interest_expense',
                                       'var_139_total_interest_income',
                                       'var_156_remaining_cash',
                                       'var_157_available_cash',
                                       'var_158_draw_down',
                                       'var_159_repayment',
                                       'var_15_other',
                                       'var_164_interest_payment',
                                       'var_165_remaining_cash',
                                       'var_166_avaialble_cash',
                                       'var_167_cfo',
                                       'var_168_cfi',
                                       'var_16_retained_earnings',
                                       'var_171_cash_bb',
                                       'var_172_plug_interest_rate',
                                       'var_173_interest_on_cash',
                                       'var_17_paid_in_capital',
                                       'var_183_cash_from_bs',
                                       'var_190_net_cash_balance',
                                       'var_195_cash_from_bs',
                                       'var_198_tolerance',
                                       'var_1_non_current_assets',
                                       'var_200_remaining_cash',
                                       'var_215_cf_tax_payment',
                                       'var_218_base',
                                       'var_219_cash_eb',
                                       'var_226_loan_bb',
                                       'var_227_draw_down',
                                       'var_228_remaining_cash',
                                       'var_229_available_cash',
                                       'var_230_revolver_dd',
                                       'var_231_revolver_repayment',
                                       'var_236_cash_bb',
                                       'var_239_revolver',
                                       'var_240_revolver_bb',
                                       'var_241_draw_down',
                                       'var_242_repayment',
                                       'var_247_plug_interest_rate',
                                       'var_253_revolver_interest',
                                       'var_257_interest_expense',
                                       'var_259_base',
                                       'var_266_base',
                                       'var_269_repayment',
                                       'var_290_revolver_interest',
                                       'var_292_cash_interest',
                                       'var_308_income_tax_rate',
                                       'var_309_taxable_income',
                                       'var_310_income_tax_expense',
                                       'var_323_cf_revolver_interest',
                                       'var_327_cf_interest_on_cash',
                                       'var_357_total_assets',
                                       'var_358_total_liabilities',
                                       'var_359_total_equity',
                                       'var_365_tolerance',
                                       'var_375_cash_from_cf',
                                       'var_378_tolerance',
                                       'var_380_remaining_cash',
                                       'var_4_cash',
                                       'var_58_retained_earnings_bb',
                                       'var_59_net_income',
                                       'var_5_non_current_liabilities',
                                       'var_65_ebit',
                                       'var_66_tax_payment',
                                       'var_67_delta_working_capital',
                                       'var_68_depreciation',
                                       'var_69_amortization',
                                       'var_6_non_cash',
                                       'var_70_total_cfo',
                                       'var_98_cash_flow_from_operation',
                                       'var_99_cash_flow_from_investing'),
                         'minimum_iteration': 10, }
        expectation = """Option Explicit

Dim max_loop
Dim tolerance
Dim iteration
Dim target_value

Dim previous_0_var_66_tax_payment 
Dim previous_1_var_70_total_cfo 
Dim previous_2_var_119_ebt 
Dim previous_3_var_138_total_interest_expense 
Dim previous_4_var_139_total_interest_income 
Dim previous_5_var_156_remaining_cash 
Dim previous_6_var_159_repayment 
Dim previous_7_var_165_remaining_cash 
Dim previous_8_var_173_interest_on_cash 
Dim previous_9_var_215_cf_tax_payment 
Dim previous_10_var_218_base 
Dim previous_11_var_228_remaining_cash 
Dim previous_12_var_230_revolver_dd 
Dim previous_13_var_231_revolver_repayment 
Dim previous_14_var_239_revolver 
Dim previous_15_var_253_revolver_interest 
Dim previous_16_var_259_base 
Dim previous_17_var_310_income_tax_expense 
Dim previous_18_var_323_cf_revolver_interest 
Dim previous_19_var_327_cf_interest_on_cash 


Dim delta
Dim delta_0_var_66_tax_payment 
Dim delta_1_var_70_total_cfo 
Dim delta_2_var_119_ebt 
Dim delta_3_var_138_total_interest_expense 
Dim delta_4_var_139_total_interest_income 
Dim delta_5_var_156_remaining_cash 
Dim delta_6_var_159_repayment 
Dim delta_7_var_165_remaining_cash 
Dim delta_8_var_173_interest_on_cash 
Dim delta_9_var_215_cf_tax_payment 
Dim delta_10_var_218_base 
Dim delta_11_var_228_remaining_cash 
Dim delta_12_var_230_revolver_dd 
Dim delta_13_var_231_revolver_repayment 
Dim delta_14_var_239_revolver 
Dim delta_15_var_253_revolver_interest 
Dim delta_16_var_259_base 
Dim delta_17_var_310_income_tax_expense 
Dim delta_18_var_323_cf_revolver_interest 
Dim delta_19_var_327_cf_interest_on_cash 

Dim var_100_cash_flow_from_financing
Dim var_101_cash_bb
Dim var_107_revenue
Dim var_108_cost_of_goods
Dim var_10_other_cl
Dim var_110_sga
Dim var_111_other_expenses
Dim var_112_other_incomes
Dim var_114_depreciation
Dim var_115_amortization
Dim var_116_ebit
Dim var_117_interest_income
Dim var_118_interest_expense
Dim var_119_ebt
Dim var_11_plug__revolver
Dim var_120_tax
Dim var_138_total_interest_expense
Dim var_139_total_interest_income
Dim var_156_remaining_cash
Dim var_157_available_cash
Dim var_158_draw_down
Dim var_159_repayment
Dim var_15_other
Dim var_164_interest_payment
Dim var_165_remaining_cash
Dim var_166_avaialble_cash
Dim var_167_cfo
Dim var_168_cfi
Dim var_16_retained_earnings
Dim var_171_cash_bb
Dim var_172_plug_interest_rate
Dim var_173_interest_on_cash
Dim var_17_paid_in_capital
Dim var_183_cash_from_bs
Dim var_190_net_cash_balance
Dim var_195_cash_from_bs
Dim var_198_tolerance
Dim var_1_non_current_assets
Dim var_200_remaining_cash
Dim var_215_cf_tax_payment
Dim var_218_base
Dim var_219_cash_eb
Dim var_226_loan_bb
Dim var_227_draw_down
Dim var_228_remaining_cash
Dim var_229_available_cash
Dim var_230_revolver_dd
Dim var_231_revolver_repayment
Dim var_236_cash_bb
Dim var_239_revolver
Dim var_240_revolver_bb
Dim var_241_draw_down
Dim var_242_repayment
Dim var_247_plug_interest_rate
Dim var_253_revolver_interest
Dim var_257_interest_expense
Dim var_259_base
Dim var_266_base
Dim var_269_repayment
Dim var_290_revolver_interest
Dim var_292_cash_interest
Dim var_308_income_tax_rate
Dim var_309_taxable_income
Dim var_310_income_tax_expense
Dim var_323_cf_revolver_interest
Dim var_327_cf_interest_on_cash
Dim var_357_total_assets
Dim var_358_total_liabilities
Dim var_359_total_equity
Dim var_365_tolerance
Dim var_375_cash_from_cf
Dim var_378_tolerance
Dim var_380_remaining_cash
Dim var_4_cash
Dim var_58_retained_earnings_bb
Dim var_59_net_income
Dim var_5_non_current_liabilities
Dim var_65_ebit
Dim var_66_tax_payment
Dim var_67_delta_working_capital
Dim var_68_depreciation
Dim var_69_amortization
Dim var_6_non_cash
Dim var_70_total_cfo
Dim var_98_cash_flow_from_operation
Dim var_99_cash_flow_from_investing

Function user_defined_function( _
var_65_ebit, var_67_delta_working_capital, var_68_depreciation, var_69_amortization, var_116_ebit, var_158_draw_down,  _
	var_164_interest_payment, var_166_avaialble_cash, var_168_cfi, var_171_cash_bb, var_172_plug_interest_rate,  _
	var_240_revolver_bb, var_247_plug_interest_rate, var_257_interest_expense, var_269_repayment, var_308_income_tax_rate) 
	max_loop = 10000
	tolerance = 0.001

	For iteration = 1 To max_loop

		' Values before calculation
		previous_0_var_66_tax_payment  = var_66_tax_payment 
		previous_1_var_70_total_cfo  = var_70_total_cfo 
		previous_2_var_119_ebt  = var_119_ebt 
		previous_3_var_138_total_interest_expense  = var_138_total_interest_expense 
		previous_4_var_139_total_interest_income  = var_139_total_interest_income 
		previous_5_var_156_remaining_cash  = var_156_remaining_cash 
		previous_6_var_159_repayment  = var_159_repayment 
		previous_7_var_165_remaining_cash  = var_165_remaining_cash 
		previous_8_var_173_interest_on_cash  = var_173_interest_on_cash 
		previous_9_var_215_cf_tax_payment  = var_215_cf_tax_payment 
		previous_10_var_218_base  = var_218_base 
		previous_11_var_228_remaining_cash  = var_228_remaining_cash 
		previous_12_var_230_revolver_dd  = var_230_revolver_dd 
		previous_13_var_231_revolver_repayment  = var_231_revolver_repayment 
		previous_14_var_239_revolver  = var_239_revolver 
		previous_15_var_253_revolver_interest  = var_253_revolver_interest 
		previous_16_var_259_base  = var_259_base 
		previous_17_var_310_income_tax_expense  = var_310_income_tax_expense 
		previous_18_var_323_cf_revolver_interest  = var_323_cf_revolver_interest 
		previous_19_var_327_cf_interest_on_cash  = var_327_cf_interest_on_cash 

		' Calculations
		var_66_tax_payment = var_215_cf_tax_payment+0
		var_70_total_cfo = var_65_ebit+var_66_tax_payment+var_67_delta_working_capital+var_69_amortization+var_68_depreciation
		var_119_ebt = var_116_ebit-var_118_interest_expense+var_117_interest_income
		var_138_total_interest_expense = var_257_interest_expense+var_253_revolver_interest
		var_139_total_interest_income = var_173_interest_on_cash+0
		var_156_remaining_cash = var_157_available_cash+var_158_draw_down+var_159_repayment+var_164_interest_payment+var_290_revolver_interest+var_292_cash_interest
		var_159_repayment = min(max(var_157_available_cash+var_158_draw_down, 0), var_269_repayment)*-1
		var_165_remaining_cash = var_166_avaialble_cash+var_167_cfo+var_168_cfi
		var_173_interest_on_cash = var_172_plug_interest_rate*var_218_base
		var_215_cf_tax_payment = -1*var_310_income_tax_expense
		var_218_base = (var_219_cash_eb+var_171_cash_bb)/2
		var_228_remaining_cash = var_229_available_cash+var_230_revolver_dd+var_231_revolver_repayment
		var_230_revolver_dd = -1*min(0, var_229_available_cash)
		var_231_revolver_repayment = -1*min(max(var_240_revolver_bb, 0), max(var_229_available_cash, 0))
		var_239_revolver = var_240_revolver_bb+var_241_draw_down+var_242_repayment
		var_253_revolver_interest = var_259_base*var_247_plug_interest_rate
		var_259_base = (var_240_revolver_bb+var_239_revolver)/2
		var_310_income_tax_expense = var_308_income_tax_rate*var_309_taxable_income
		var_323_cf_revolver_interest = var_253_revolver_interest*-1
		var_327_cf_interest_on_cash = var_173_interest_on_cash+0

		var_98_cash_flow_from_operation=var_70_total_cfo
		var_117_interest_income=var_139_total_interest_income
		var_118_interest_expense=var_138_total_interest_expense
		var_157_available_cash=var_165_remaining_cash
		var_167_cfo=var_98_cash_flow_from_operation
		var_219_cash_eb=var_228_remaining_cash
		var_229_available_cash=var_156_remaining_cash
		var_241_draw_down=var_230_revolver_dd
		var_242_repayment=var_231_revolver_repayment
		var_290_revolver_interest=var_323_cf_revolver_interest
		var_292_cash_interest=var_327_cf_interest_on_cash
		var_309_taxable_income=var_119_ebt

		' Compare values after calculations
		delta_0_var_66_tax_payment  = Abs(previous_0_var_66_tax_payment  - var_66_tax_payment )
		delta_1_var_70_total_cfo  = Abs(previous_1_var_70_total_cfo  - var_70_total_cfo )
		delta_2_var_119_ebt  = Abs(previous_2_var_119_ebt  - var_119_ebt )
		delta_3_var_138_total_interest_expense  = Abs(previous_3_var_138_total_interest_expense  - var_138_total_interest_expense )
		delta_4_var_139_total_interest_income  = Abs(previous_4_var_139_total_interest_income  - var_139_total_interest_income )
		delta_5_var_156_remaining_cash  = Abs(previous_5_var_156_remaining_cash  - var_156_remaining_cash )
		delta_6_var_159_repayment  = Abs(previous_6_var_159_repayment  - var_159_repayment )
		delta_7_var_165_remaining_cash  = Abs(previous_7_var_165_remaining_cash  - var_165_remaining_cash )
		delta_8_var_173_interest_on_cash  = Abs(previous_8_var_173_interest_on_cash  - var_173_interest_on_cash )
		delta_9_var_215_cf_tax_payment  = Abs(previous_9_var_215_cf_tax_payment  - var_215_cf_tax_payment )
		delta_10_var_218_base  = Abs(previous_10_var_218_base  - var_218_base )
		delta_11_var_228_remaining_cash  = Abs(previous_11_var_228_remaining_cash  - var_228_remaining_cash )
		delta_12_var_230_revolver_dd  = Abs(previous_12_var_230_revolver_dd  - var_230_revolver_dd )
		delta_13_var_231_revolver_repayment  = Abs(previous_13_var_231_revolver_repayment  - var_231_revolver_repayment )
		delta_14_var_239_revolver  = Abs(previous_14_var_239_revolver  - var_239_revolver )
		delta_15_var_253_revolver_interest  = Abs(previous_15_var_253_revolver_interest  - var_253_revolver_interest )
		delta_16_var_259_base  = Abs(previous_16_var_259_base  - var_259_base )
		delta_17_var_310_income_tax_expense  = Abs(previous_17_var_310_income_tax_expense  - var_310_income_tax_expense )
		delta_18_var_323_cf_revolver_interest  = Abs(previous_18_var_323_cf_revolver_interest  - var_323_cf_revolver_interest )
		delta_19_var_327_cf_interest_on_cash  = Abs(previous_19_var_327_cf_interest_on_cash  - var_327_cf_interest_on_cash )

		' Cumulative absolute differences (deltas)
		delta = 0
		delta = delta + delta_0_var_66_tax_payment 
		delta = delta + delta_1_var_70_total_cfo 
		delta = delta + delta_2_var_119_ebt 
		delta = delta + delta_3_var_138_total_interest_expense 
		delta = delta + delta_4_var_139_total_interest_income 
		delta = delta + delta_5_var_156_remaining_cash 
		delta = delta + delta_6_var_159_repayment 
		delta = delta + delta_7_var_165_remaining_cash 
		delta = delta + delta_8_var_173_interest_on_cash 
		delta = delta + delta_9_var_215_cf_tax_payment 
		delta = delta + delta_10_var_218_base 
		delta = delta + delta_11_var_228_remaining_cash 
		delta = delta + delta_12_var_230_revolver_dd 
		delta = delta + delta_13_var_231_revolver_repayment 
		delta = delta + delta_14_var_239_revolver 
		delta = delta + delta_15_var_253_revolver_interest 
		delta = delta + delta_16_var_259_base 
		delta = delta + delta_17_var_310_income_tax_expense 
		delta = delta + delta_18_var_323_cf_revolver_interest 
		delta = delta + delta_19_var_327_cf_interest_on_cash 

		' If cumulative differences is smaller than tolerance, then exit function.
		If iteration > 10 And delta < tolerance Then
			target_value = var_156_remaining_cash
			user_defined_function = var_156_remaining_cash
			Exit Function
		End If
	Next iteration
End Function

Function Min(ParamArray values() As Variant) As Variant
   Dim minValue, Value As Variant
   minValue = values(0)
   For Each Value In values
       If Value < minValue Then minValue = Value
   Next
   Min = minValue
End Function

Function Max(ParamArray values() As Variant) As Variant
   Dim maxValue, Value As Variant
   maxValue = values(0)
   For Each Value In values
       If Value > maxValue Then maxValue = Value
   Next
   Max = maxValue
End Function
"""
        self.udf_builder.export(**request_model)
        self.assertEqual(self.udf_builder.text, expectation)


if __name__ == '__main__':
    unittest.main()
