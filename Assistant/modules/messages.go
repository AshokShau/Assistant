package modules

import (
	"fmt"
	"github.com/AshokShau/Assistant/Assistant/config"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
)

func PmMessage(bot *gotgbot.Bot, ctx *ext.Context) error {
	msg := ctx.EffectiveMessage
	user := ctx.EffectiveSender.User
	chat := ctx.EffectiveChat

	if config.OwnerId == user.Id {
		reply := msg.ReplyToMessage
		if reply != nil && reply.ForwardOrigin != nil {
			msgOrigen := reply.ForwardOrigin.MergeMessageOrigin()
			if msgOrigen.SenderUser != nil {
				if _, err := bot.CopyMessage(msgOrigen.SenderUser.Id, chat.Id, msg.MessageId, &gotgbot.CopyMessageOpts{}); err != nil {
					return fmt.Errorf("error copying message: %v", err)
				}
			}
		}
	} else {
		if _, err := bot.ForwardMessage(config.OwnerId, chat.Id, msg.MessageId, &gotgbot.ForwardMessageOpts{}); err != nil {
			return fmt.Errorf("error forwarding message: %v", err)
		}
	}
	return ext.EndGroups
}
