def pytest_addoption(parser):
    group = parser.getgroup('enable starting tests from a specified point')
    group.addoption('--start-from-file', dest='start-from-file', type=str,
                    help='The path to the file to start from')
    group.addoption('--start-from-test-case', dest='start-from-test-case',
                    type=str, help='The test case (in the form '
                                   'TestCaseClass.test_method_name) to start '
                                   'from')


def pytest_collection_modifyitems(session, config, items):
    start_from_file = config.getoption('start-from-file')
    start_from_test_case = config.getoption('start-from-test-case')

    if not (start_from_file or start_from_test_case):
        return

    if start_from_file:
        try:
            paths = [item.location[0] for item in items]
            start_index = paths.index(start_from_file)
        except ValueError:
            raise ValueError('Specified file %s was not in the list' %
                             start_from_file)
    else:
        try:
            test_cases = [item.location[2] for item in items]
            start_index = test_cases.index(start_from_test_case)
        except ValueError:
            raise ValueError('Specified test case %s was not in the list' %
                             start_from_test_case)

    before_start = items[:start_index]
    after_start = items[start_index:]

    # We need to modify items in place.
    del items[:]

    # Run items *from* starting index.
    items.extend(after_start + before_start)

    start_from = start_from_file or start_from_test_case
    print('Running %d items from %s' % (len(items), start_from))
