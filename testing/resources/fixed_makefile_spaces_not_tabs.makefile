all: foo bar

foo: bar
	echo "foo"
	echo "this line uses spaces not tabs"

bar:
	echo "bar"
