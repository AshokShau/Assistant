package config

import (
	"strconv"
)

// typeConvertor is a struct that will convert a string to a specific type
type typeConvertor struct {
	str string
}

// Int64 Int64Array will return an int64 array from a comma separated string
func (t typeConvertor) Int64() int64 {
	val, _ := strconv.ParseInt(t.str, 10, 64)
	return val
}
