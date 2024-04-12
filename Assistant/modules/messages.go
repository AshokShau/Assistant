package modules

import (
	log "github.com/sirupsen/logrus"

	"github.com/Abishnoi69/Assistant/Assistant/config"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
)

func PmMessage(bot *gotgbot.Bot, ctx *ext.Context) error {
	msg := ctx.EffectiveMessage
	user := ctx.EffectiveSender.User
	chat := ctx.EffectiveChat

	if config.OwnerId == user.Id {
		reply := msg.ReplyToMessage

		if reply == msg.ReplyToMessage {
			if msg.ReplyToMessage.ForwardOrigin != nil {
				msgOrigen := msg.ReplyToMessage.ForwardOrigin.MergeMessageOrigin()
				if msgOrigen.SenderUser != nil {
					_, err := bot.CopyMessage(msgOrigen.SenderUser.Id, chat.Id, msg.MessageId, &gotgbot.CopyMessageOpts{})
					if err != nil {
						log.Error(err)
						return err
					}
				}
			}
		}
	} else {

		_, err := bot.ForwardMessage(config.OwnerId, chat.Id, msg.MessageId, &gotgbot.ForwardMessageOpts{})

		if err != nil {
			log.Error(err)
			return err
		}
	}
	return ext.EndGroups
}
