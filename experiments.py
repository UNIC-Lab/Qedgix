import os
import argparse

N = 10

def arguments():
	cli = argparse.ArgumentParser()

	# the environment to use (separate run for each arg)
	cli.add_argument(
		"--env",
		nargs="*",
		type=str,
		default=["sc2"],
	)

	# the config file to use (separate run for each arg)
	cli.add_argument(
		"--config",
		nargs="*",
		type=str,
		default=["qgnn"],
	)

	# extra config arguments
	for i in range(N):
		cli.add_argument(
			"--params%d" % (i+1),
			nargs="*",
			type=str,
			default=[],
		)

	args = cli.parse_args()
	return args


def build_cmd(env, config, params):
	print("python pymarl/main.py --config={config} --env-config={env} with {params}".format(env=env, config=config,
																					  params=" ".join(params)))
	return "python pymarl/main.py --config={config} --env-config={env} with {params}".format(env=env, config=config, params=" ".join(params))
	# return "/usr/local/bin/python3.9 src/main.py --config={config} --env-config={env} with {params}".format(env=env, config=config, params=" ".join(params))


def run_cmd(cmd):
	os.system(cmd)


def build_params(args, params_list, i):
	if i == N:
		return params_list
	argname_i = "params%d" % (i+1)
	params_i = getattr(args, argname_i)
	if len(params_i) > 0:
		new_list = []
		for params in params_list:
			for param_i in params_i:
				new_list.append(params + [param_i])
		return build_params(args, new_list, i+1)
	else:
		return build_params(args, params_list, i+1)


if __name__ == '__main__':
	args = arguments()
	for env in args.env:
		for config in args.config:
			params_list = build_params(args, [[]], 0)
			for params in params_list:
				run_cmd(build_cmd(env, config, params))
			


