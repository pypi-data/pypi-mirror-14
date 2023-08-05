from errbot import BotPlugin, cmdfilter
BLOCK_COMMAND = (None, None, None)


def get_acl_usr(msg):
    if hasattr(msg.frm, 'aclattr'):  # if the identity requires a special field to be used for acl
        return msg.frm.aclattr
    return msg.frm.person  # default


class ACLS(BotPlugin):
    """ This checks commands for potential ACL violations.
    """

    def access_denied(self, msg, reason, dry_run):
        if not dry_run or not self.bot_config.HIDE_RESTRICTED_ACCESS:
            self._bot.send_simple_reply(msg, reason)
        return BLOCK_COMMAND

    @cmdfilter
    def acls(self, msg, cmd, args, dry_run):
        """
        Check command against ACL rules

        :param msg: The original message the commands is coming from.
        :param cmd: The command name
        :param args: Its arguments.
        :param dry_run: pass True to not act on the check (messages / deferred auth etc.)

        Return None, None, None if the command is blocked or deferred
        """
        self.log.debug("Check %s for ACLs." % cmd)

        usr = get_acl_usr(msg)
        typ = msg.type

        self.log.debug("Matching ACLs against username %s" % usr)

        if cmd not in self.bot_config.ACCESS_CONTROLS:
            self.bot_config.ACCESS_CONTROLS[cmd] = self.bot_config.ACCESS_CONTROLS_DEFAULT

        if ('allowusers' in self.bot_config.ACCESS_CONTROLS[cmd] and
           usr not in self.bot_config.ACCESS_CONTROLS[cmd]['allowusers']):
            return self.access_denied(msg, "You're not allowed to access this command from this user", dry_run)

        if ('denyusers' in self.bot_config.ACCESS_CONTROLS[cmd] and
           usr in self.bot_config.ACCESS_CONTROLS[cmd]['denyusers']):
            return self.access_denied(msg, "You're not allowed to access this command from this user", dry_run)

        if typ == 'groupchat':
            if not hasattr(msg.frm, 'room'):
                raise Exception('msg.frm is not a MUCIdentifier as it misses the "room" property. Class of frm : %s'
                                % msg.frm.__class__)
            room = str(msg.frm.room)
            if ('allowmuc' in self.bot_config.ACCESS_CONTROLS[cmd] and
               self.bot_config.ACCESS_CONTROLS[cmd]['allowmuc'] is False):
                return self.access_denied(msg, "You're not allowed to access this command from a chatroom", dry_run)

            if ('allowrooms' in self.bot_config.ACCESS_CONTROLS[cmd] and
               room not in self.bot_config.ACCESS_CONTROLS[cmd]['allowrooms']):
                return self.access_denied(msg, "You're not allowed to access this command from this room", dry_run)

            if ('denyrooms' in self.bot_config.ACCESS_CONTROLS[cmd] and
               room in self.bot_config.ACCESS_CONTROLS[cmd]['denyrooms']):
                return self.access_denied(msg, "You're not allowed to access this command from this room", dry_run)

        elif ('allowprivate' in self.bot_config.ACCESS_CONTROLS[cmd] and
              self.bot_config.ACCESS_CONTROLS[cmd]['allowprivate'] is False):
            return self.access_denied(
                    msg,
                    "You're not allowed to access this command via private message to me", dry_run)

        return msg, cmd, args

    @cmdfilter
    def admin(self, msg, cmd, args, dry_run):
        """
        Check command against the is_admin criteria.

        :param msg: The original message the commands is coming from.
        :param cmd: The command name
        :param args: Its arguments.
        :param dry_run: pass True to not act on the check (messages / deferred auth etc.)

        """
        self.log.info("Check if %s is admin only command." % cmd)
        f = self._bot.all_commands[cmd]

        if f._err_command_admin_only:
            if msg.type == 'groupchat':
                return self.access_denied(
                        msg,
                        "You cannot administer the bot from a chatroom, message the bot directly", dry_run)

            if get_acl_usr(msg) not in self.bot_config.BOT_ADMINS:
                return self.access_denied(msg, "This command requires bot-admin privileges", dry_run)

        return msg, cmd, args
