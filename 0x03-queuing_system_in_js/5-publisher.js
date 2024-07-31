import redis from 'redis';

// Create a Redis client
const publisher = redis.createClient();

// Handle connection event
publisher.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle error event
publisher.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Function to publish messages
const publishMessage = (message, time) => {
  setTimeout(() => {
    console.log(`About to send ${message}`);
    publisher.publish('holberton school channel', message);
  }, time);
};

// Publish messages with delays
publishMessage('Holberton Student #1 starts course', 100);
publishMessage('Holberton Student #2 starts course', 200);
publishMessage('KILL_SERVER', 300);
publishMessage('Holberton Student #3 starts course', 400);
