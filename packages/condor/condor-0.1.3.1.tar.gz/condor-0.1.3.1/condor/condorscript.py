from condor import condor_config

def condor_test_action(args):
    print('Test action with args: {0}'.format(args))
    print('Got action from command line: {0}'.format(args['argv']))
    return {'message' : 'Greetings'}

def condor_another_test_action(args):
    print('Another test action got next pipe args: {0}'.format(args['pipe_args']))
    return {}

def condor_failing_action(args):
	result = 1 / 0
	return {}

condor_config.setup(
	name='test',
	wdir='.',
	task=[ {
		'name' : 'condor-test',
		'desc' : 'Test task',
		'args' : {'test_arg' : 'test'},
		'actions' : [
            condor_test_action],
		'pipe' : False
		},
		{
		'name' : 'condor-test-2',
		'desc' : 'Another test task',
		'args' : {},
		'actions' : [
            condor_another_test_action],
		'pipe' : True
		},
        {
        'name' : 'condor-main-task',
        'desc' : 'Main example task',
        'args' : {},
        'actions' : [
            'condor-test',
            'condor-test-2',
            condor_failing_action],
        'pipe' : False
        }
	]
)