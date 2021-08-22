all: foo bar baz

foo:
	echo "foo"

bar: baz
	echo "bar"
	echo "baz"

baz:
	echo "baz"
