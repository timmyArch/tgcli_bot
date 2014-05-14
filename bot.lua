function on_msg_receive (msg)
	if not (msg == nil) then
		sender =""
		message = msg.text
		message = string.gsub(message, "\'" , "") 
		message = string.gsub(message, "\"" , "") 
		number = 0 
		if not msg.from.phone == nil then
			number = msg.from.phone
		end 
		if msg.to.type == "chat" then
			sender = msg.to.title
			sender_2 = msg.from.print_name
		elseif msg.to.type == "encr_chat" then
			sender = msg.to.print_name
			sender_2 = msg.from.print_name
		else 
			sender = msg.from.print_name
			sender_2 = sender
		end
		if sender == "TimmyServer" then
			return
		end         
		local value = io.popen("python /var/www/tgcli_bot/bot.py -n " .. sender .. " -s " .. sender_2 .." -m '".. message.."'" )
		local result = value:read("*a")
		value:close()
		rep = result:match("{{photo}}([^,]+)")
		if rep then
			a = rep:match("([A-z/0-9]+\.gif)")
			if a then
				send_photo (rep,a)
			end
			a = rep:match("([A-z/0-9]+\.png)")
			if a then
				send_photo (rep,a)
			end
			a = rep:match("([A-z/0-9]+\.jpeg)")
			if a then
				send_photo (rep,a)
			end
			a = rep:match("([A-z/0-9]+\.jpg)")
			if a then
				send_photo (rep,a)
			end
		else
			if not (result == nil or result == "" ) then
				send_msg (sender,result)
			end
		end 
	end 
end

function on_second_scheduler_end ()
	for variable = 0, 10, 1 do
		local file = io.popen('FILE=/tmp/luabot.tmp; head -n1 $FILE && sed -i "1d" $FILE')
		local output = file:read('*all')
		repicent, message = output:match("([^,]+),([^,]+)")
		if not repicent or not message or repicent == "" or message == "" then
			return
		end
		rep = repicent:match("{{photo}}([^,]+)")
		if rep then
			a = message:match("([A-z/0-9]+\.gif)")
			if a then
				send_photo (rep,a)
			end
			a = message:match("([A-z/0-9]+\.png)")
			if a then
				send_photo (rep,a)
			end
			a = message:match("([A-z/0-9]+\.jpeg)")
			if a then
				send_photo (rep,a)
			end
			a = message:match("([A-z/0-9]+\.jpg)")
			if a then
				send_photo (rep,a)
			end
		else
			send_msg (repicent,message)
		end
		file:close()
	end
end

function on_our_id (id)
				our_id = id
				end

function on_secret_chat_created (peer)
				end

function on_user_update (user)
				end

function on_chat_update (user)
				end

function on_get_difference_end ()
				end

function on_binlog_replay_end ()
				end
