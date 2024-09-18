package config

import (
	"os"
	"strconv"

	_ "github.com/joho/godotenv/autoload"
)

var (
	Token   = getEnv("TOKEN", "")
	OwnerId = getEnvInt64("OWNER_ID", 5938660179)
)

// getEnv returns the value of an environment variable or a default value if it is not set
func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// getEnvInt64 returns the value of an environment variable as an int64 or a default value if it is not set
func getEnvInt64(key string, defaultValue int64) int64 {
	if value, err := strconv.ParseInt(os.Getenv(key), 10, 64); err == nil {
		return value
	}
	return defaultValue
}
