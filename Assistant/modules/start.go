package modules

import (
	"fmt"

	"strconv"
	"time"

	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
)

var StartTime = time.Now().Unix()

func Start(bot *gotgbot.Bot, ctx *ext.Context) error {
	upTime := int(time.Now().Unix()) - int(StartTime)
	msg := "I am alive baby alive since:" + strconv.Itoa(upTime) + "seconds"

	_, err := ctx.EffectiveMessage.Reply(bot, msg, nil)
	if err != nil {
		return fmt.Errorf("failed to Start message: %w", err)
	}

	return nil
}
