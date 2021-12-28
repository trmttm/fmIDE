# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\Yamaka\\Documents\\FM'],
             binaries=[],
             datas=[],
             hiddenimports=['xlsxwriter',],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
# a.datas += [('vbaProject.bin', '.\\vbaProject.bin', 'DATA')]

a.datas += [('/Pickles/Audit BS', '.\\Pickles\\Audit BS', 'DATA')]
a.datas += [('/Pickles/Audit Cash', '.\\Pickles\\Audit Cash', 'DATA')]
a.datas += [('/Pickles/Balance Sheet', '.\\Pickles\\Balance Sheet', 'DATA')]
a.datas += [('/Pickles/Balance Sheet - Assets', '.\\Pickles\\Balance Sheet - Assets', 'DATA')]
a.datas += [('/Pickles/Balance Sheet - Equity', '.\\Pickles\\Balance Sheet - Equity', 'DATA')]
a.datas += [('/Pickles/Balance Sheet - Liabilities', '.\\Pickles\\Balance Sheet - Liabilities', 'DATA')]
a.datas += [('/Pickles/Base', '.\\Pickles\\Base', 'DATA')]
a.datas += [('/Pickles/Base2', '.\\Pickles\\Base2', 'DATA')]
a.datas += [('/Pickles/Base3', '.\\Pickles\\Base3', 'DATA')]
a.datas += [('/Pickles/Cash Flow Statement', '.\\Pickles\\Cash Flow Statement', 'DATA')]
a.datas += [('/Pickles/CFWF', '.\\Pickles\\CFWF', 'DATA')]
a.datas += [('/Pickles/Corkscrew', '.\\Pickles\\Corkscrew', 'DATA')]
a.datas += [('/Pickles/Income Statement', '.\\Pickles\\Income Statement', 'DATA')]
a.datas += [('/Pickles/Math - Weighted Average', '.\\Pickles\\Math - Weighted Average', 'DATA')]
a.datas += [('/Pickles/pickle_for_unit_test', '.\\Pickles\\pickle_for_unit_test', 'DATA')]
a.datas += [('/Pickles/pickle_from_gui', '.\\Pickles\\pickle_from_gui', 'DATA')]
a.datas += [('/Pickles/pickle_from_gui_all', '.\\Pickles\\pickle_from_gui_all', 'DATA')]
a.datas += [('/Pickles/Plug', '.\\Pickles\\Plug', 'DATA')]
a.datas += [('/Pickles/Retained Earnings', '.\\Pickles\\Retained Earnings', 'DATA')]
a.datas += [('/Pickles/Template Name', '.\\Pickles\\Template Name', 'DATA')]
a.datas += [('/Pickles/Test', '.\\Pickles\\Test', 'DATA')]
a.datas += [('/Pickles/Test Model', '.\\Pickles\\Test Model', 'DATA')]
a.datas += [('/Pickles/test_module', '.\\Pickles\\test_module', 'DATA')]
a.datas += [('/Pickles/test_module_saved_as_a_module', '.\\Pickles\\test_module_saved_as_a_module', 'DATA')]
a.datas += [('/Pickles/Tr AP', '.\\Pickles\\Tr AP', 'DATA')]
a.datas += [('/Pickles/Tr AR', '.\\Pickles\\Tr AR', 'DATA')]
a.datas += [('/Pickles/Tr Capex Depreciation', '.\\Pickles\\Tr Capex Depreciation', 'DATA')]
a.datas += [('/Pickles/Tr COGS', '.\\Pickles\\Tr COGS', 'DATA')]
a.datas += [('/Pickles/Tr Debt Model', '.\\Pickles\\Tr Debt Model', 'DATA')]
a.datas += [('/Pickles/Tr Dividend Payout', '.\\Pickles\\Tr Dividend Payout', 'DATA')]
a.datas += [('/Pickles/Tr FG WIP RM', '.\\Pickles\\Tr FG WIP RM', 'DATA')]
a.datas += [('/Pickles/Tr Income Tax - Simple', '.\\Pickles\\Tr Income Tax - Simple', 'DATA')]
a.datas += [('/Pickles/Tr Inventory Model', '.\\Pickles\\Tr Inventory Model', 'DATA')]
a.datas += [('/Pickles/Tr OPEX Alumina', '.\\Pickles\\Tr OPEX Alumina', 'DATA')]
a.datas += [('/Pickles/Tr Plug Interest', '.\\Pickles\\Tr Plug Interest', 'DATA')]
a.datas += [('/Pickles/Tr Revenue', '.\\Pickles\\Tr Revenue', 'DATA')]
a.datas += [('/Pickles/Tr SGA', '.\\Pickles\\Tr SGA', 'DATA')]

a.datas += [('applet.ico', '.\\applet.ico', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='App',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='.\\applet.ico')
