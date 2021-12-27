from setuptools import setup

setup(
    name='fmIDE',
    version='',
    packages=['Main', 'Tests', 'Tests.pickles', 'Pickles', 'Entities', 'Entities.Line',
              'Entities.Shape', 'Entities.Format', 'Entities.Selection', 'Entities.Connection',
              'Entities.Selections', 'Entities.Worksheets', 'Entities.InputRanges',
              'Entities.InputValues', 'Entities.ShapeFormat', 'Entities.AccountOrder',
              'Entities.NumberFormat', 'Entities.AccountOrders', 'Entities.AccountValues',
              'Entities.ConnectionIDs', 'Entities.InputDecimals', 'Entities.VerticalAccounts',
              'Entities.RectangleSelector', 'Presenter', 'Presenter.Macros', 'Presenter.States',
              'Presenter.AddShape', 'Presenter.Commands', 'Presenter.DrawLine', 'Presenter.Template',
              'Presenter.MoveShape', 'Presenter.InputEntry', 'Presenter.Worksheets',
              'Presenter.ClearCanvas', 'Presenter.RemoveShape', 'Presenter.ConnectShape',
              'Presenter.FeedbackUser', 'Presenter.DrawRectangle', 'Presenter.HighlightShape',
              'Presenter.UpdateAccountOrder', 'Presenter.UpdateAccountsList',
              'Presenter.LoadPickleFilesList', 'Presenter.UpdateConnectionIDs',
              'Presenter.PresenterPassThrough', 'Presenter.UpdateShapeProperties',
              'Presenter.UpdateAccountsListWithDeltas', 'Resources', 'Utilities', 'Utilities.Graphs',
              'Utilities.Memento', 'ViewModel', 'Controller', 'Controller.MouseController',
              'Interactor', 'RequestModel', 'EntityGateway', 'ResponseModel', 'BoundaryOutput',
              'ExternalSystems', 'ExternalSystems.Configurations',
              'ExternalSystems.Configurations.ConfigTest', 'ExternalSystems.UserDefinedFunction',
              'ExternalSystems.UserDefinedFunction.Test', 'PicklesCommands', 'Templates'],
    url='',
    license='',
    author='STTM',
    author_email='',
    description=''
)
