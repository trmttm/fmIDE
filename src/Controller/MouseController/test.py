import unittest


class TestInteractor:
    def __init__(self):
        self._request_model = None

    def execute(self, request):
        self._request_model = request['handler']

    @property
    def request_model(self):
        return self._request_model

    def reset_request_model(self):
        self._request_model = None


def create_test_cases():
    from ...Controller.MouseController import constants as cns
    request1 = {'x': 10, 'y': 15, cns.BUTTON: cns.LEFT, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK}
    request2 = {'x': 10, 'y': 15, cns.BUTTON: cns.LEFT, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK_MOTION}
    request3 = {'x': 10, 'y': 15, cns.BUTTON: cns.LEFT, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK_RELEASE}
    request4 = {'x': 10, 'y': 15, cns.BUTTON: cns.RIGHT, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK}
    request5 = {'x': 10, 'y': 15, cns.BUTTON: cns.RIGHT, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK_MOTION}
    request6 = {'x': 10, 'y': 15, cns.BUTTON: cns.RIGHT, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK_RELEASE}
    request7 = {'x': 10, 'y': 15, cns.BUTTON: cns.MIDDLE, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK}
    request8 = {'x': 10, 'y': 15, cns.BUTTON: cns.MIDDLE, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK_MOTION}
    request9 = {'x': 10, 'y': 15, cns.BUTTON: cns.MIDDLE, cns.MODIFIER: cns.SHIFT, cns.GESTURE: cns.CLICK_RELEASE}

    expected_request_model1 = 'LeftClickHandler'
    expected_request_model2 = 'LeftMotionHandler'
    expected_request_model3 = 'LeftReleaseHandler'
    expected_request_model4 = 'RightClickHandler'
    expected_request_model5 = 'RightMotionHandler'
    expected_request_model6 = 'RightReleaseHandler'
    expected_request_model7 = 'MiddleClickHandler'
    expected_request_model8 = 'MiddleMotionHandler'
    expected_request_model9 = 'MiddleReleaseHandler'

    tests = [
        (request1, expected_request_model1),
        (request2, expected_request_model2),
        (request3, expected_request_model3),
        (request4, expected_request_model4),
        (request5, expected_request_model5),
        (request6, expected_request_model6),
        (request7, expected_request_model7),
        (request8, expected_request_model8),
        (request9, expected_request_model9),
    ]
    return tests


class MyTestCase(unittest.TestCase):
    def test_handlers(self):
        cmd = TestInteractor()
        tests = create_test_cases()

        from ...Controller.MouseController import MouseController
        from ...Controller.MouseController import constants as a
        mouse = MouseController()
        interactor_keys = [
            'LeftClickHandler',
            'LeftMotionHandler',
            'LeftReleaseHandler',
            'RightClickHandler',
            'RightMotionHandler',
            'RightReleaseHandler',
            'MiddleClickHandler',
            'MiddleMotionHandler',
            'MiddleReleaseHandler',
        ]
        d = dict(zip([i for i in range(len(interactor_keys))], interactor_keys))
        mouse.configure(*[0, cmd.execute, lambda r: r['button'] == a.LEFT and r['gesture'] == a.CLICK, {}])
        mouse.configure(*[1, cmd.execute, lambda r: r['button'] == a.LEFT and r['gesture'] == a.CLICK_MOTION, {}])
        mouse.configure(*[2, cmd.execute, lambda r: r['button'] == a.LEFT and r['gesture'] == a.CLICK_RELEASE, {}])
        mouse.configure(*[3, cmd.execute, lambda r: r['button'] == a.RIGHT and r['gesture'] == a.CLICK, {}])
        mouse.configure(*[4, cmd.execute, lambda r: r['button'] == a.RIGHT and r['gesture'] == a.CLICK_MOTION, {}])
        mouse.configure(*[5, cmd.execute, lambda r: r['button'] == a.RIGHT and r['gesture'] == a.CLICK_RELEASE, {}])
        mouse.configure(*[6, cmd.execute, lambda r: r['button'] == a.MIDDLE and r['gesture'] == a.CLICK, {}])
        mouse.configure(*[7, cmd.execute, lambda r: r['button'] == a.MIDDLE and r['gesture'] == a.CLICK_MOTION, {}])
        mouse.configure(*[8, cmd.execute, lambda r: r['button'] == a.MIDDLE and r['gesture'] == a.CLICK_RELEASE, {}])

        for test in tests:
            request, expected_request_model = test
            mouse.handle(**request)
            self.assertEqual(d[cmd.request_model], expected_request_model)
            cmd.reset_request_model()


if __name__ == '__main__':
    unittest.main()
