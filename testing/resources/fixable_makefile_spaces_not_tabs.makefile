all: foo bar baz

foo:
	echo "foo"
  echo "this line uses spaces not tabs"

bar: baz
	echo "bar"

baz:
	echo "baz"
