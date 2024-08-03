import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const app = express();
const port = 1245;

const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

const queue = kue.createQueue();

const INITIAL_SEATS = 50;
let reservationEnabled = true;

const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
};

(async () => {
  await reserveSeat(INITIAL_SEATS);
})();

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats.toString() });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  try {
    const job = queue.create('reserve_seat', {}).save((err) => {
      if (err) {
        return res.json({ status: 'Reservation failed' });
      }
      res.json({ status: 'Reservation in process' });
    });

    job.on('complete', (result) => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errorMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
  } catch (err) {
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      let availableSeats = await getCurrentAvailableSeats();

      if (availableSeats <= 0) {
        reservationEnabled = false;
        throw new Error('Not enough seats available');
      }

      await reserveSeat(availableSeats - 1);
      done();
    } catch (err) {
      done(err);
    }
  });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
