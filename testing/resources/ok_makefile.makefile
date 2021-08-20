all: foo bar baz

foo:
	echo "foo"

bar: baz
	echo "bar"

baz:
	echo "baz"
