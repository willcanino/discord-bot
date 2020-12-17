module.exports = {
    name: 'name here',
    description: "description here:",
    execute(message, args) {
        message.channel.send('response here');
    }
}



// remove roles
// message.member.roles.remove('role id');  (add to the if statement)
