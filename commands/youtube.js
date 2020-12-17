module.exports = {
    name: 'youtube',
    description: "sends the youtube channel link:",
    execute(message, args) {
        message.channel.send('<https://www.youtube.com/willcanino>');
    }
}