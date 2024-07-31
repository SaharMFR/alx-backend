import redis from 'redis';

// Create a Redis client
const subscriber = redis.createClient();

// Handle connection event
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle error event
subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
subscriber.subscribe('holberton school channel');

// Handle messages received on the channel
subscriber.on('message', (channel, message) => {
  console.log(message);

  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe();
    subscriber.quit();
  }
});
