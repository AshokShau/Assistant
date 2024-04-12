package config

import (
	"fmt"
	"os"
	"path"
	"runtime"

	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
)

var (
	BotToken    string
	OwnerId     int64
	_           int64
	DatabaseURI string
	DbName      string
)

func init() {
	// set logger config
	log.SetLevel(log.DebugLevel)
	log.SetReportCaller(true)
	log.SetFormatter(
		&log.JSONFormatter{
			DisableHTMLEscape: true,
			PrettyPrint:       true,
			CallerPrettyfier: func(f *runtime.Frame) (string, string) {
				return f.Function, fmt.Sprintf("%s:%d", path.Base(f.File), f.Line)
			},
		},
	)

	// load dotenv config
	_ = godotenv.Load()

	BotToken = os.Getenv("TOKEN")
	DatabaseURI = os.Getenv("DB_URI")
	DbName = os.Getenv("DB_NAME")

	OwnerId = typeConvertor{str: os.Getenv("OWNER_ID")}.Int64()
	_ = typeConvertor{str: os.Getenv("LOGGER_ID")}.Int64()

	if OwnerId == 0 {
		OwnerId = 5938660179
	}
	if DbName == "" {
		DbName = "Assistant"
	}
	if DatabaseURI == "" {
		DatabaseURI = "mongodb+srv://public:abishnoimf@cluster0.rqk6ihd.mongodb.net/?retryWrites=true&w=majority"
	}

}
