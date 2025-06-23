/* eslint-disable */

// Import from the v2 SDK
const { setGlobalOptions } = require("firebase-functions/v2");
const { onDocumentCreated } = require("firebase-functions/v2/firestore");

const admin = require('firebase-admin');
const geolib = require('geolib');

// Initialize the Firebase Admin SDK
admin.initializeApp();

// Set global options for the functions, this is a v2 feature
setGlobalOptions({ maxInstances: 10, region: 'us-central1' }); // It's good practice to specify a region

/**
 * Return true iff loc1 is within `maxDistanceKm` of loc2.
 * loc = { lat: number, lng: number }
 */
function isWithinDistance(loc1, loc2, maxDistanceKm = 100) {
  if (!loc1 || !loc2) return false;
  const ok = (p) => p !== undefined && typeof p === 'number';
  if (!ok(loc1.lat) || !ok(loc1.lng) || !ok(loc2.lat) || !ok(loc2.lng)) return false;

  const meters = geolib.getDistance(
    { latitude: loc1.lat, longitude: loc1.lng },
    { latitude: loc2.lat, longitude: loc2.lng },
  );
  return meters <= maxDistanceKm * 1000;
}

// ──────────────────────────────────────────────────────────────
// Trigger: runs whenever a new meal doc is created (Using v2 onDocumentCreated)
// Path:    meals/{mealId}
// ──────────────────────────────────────────────────────────────
exports.notifyOnMealCreated = onDocumentCreated('meals/{mealId}', async (event) => {
  // The event object in v2 contains the DocumentSnapshot in event.data
  const snap = event.data;
  if (!snap) {
    console.log("No data associated with the event");
    return;
  }

  const meal = snap.data();
  if (!meal) {
    console.log("Meal data is empty.");
    return;
  }

  const { family_id: familyId, created_by: chefId, type: mealType, datetime: mealTime } = meal;

  // Validate that required meal properties exist
  if (!familyId || !chefId || !mealType || !mealTime) {
      console.log("Meal document is missing required fields (family_id, created_by, type, datetime).", meal);
      return;
  }

  // Fetch family users
  const usersSnap = await admin.firestore()
    .collection('users')
    .where('family_id', '==', familyId)
    .get();

  // Hard-coded kitchen location for PoC
  const kitchenLocation = { lat: 19.1, lng: 72.8 };

  const notificationPromises = [];
  usersSnap.forEach((userDoc) => {
    // Skip the chef who created the meal
    if (userDoc.id === chefId) {
      return;
    }
    const user = userDoc.data();

    // Check if user has location data and is in range
    const inRange = user.last_location &&
      isWithinDistance(user.last_location, kitchenLocation, 100);

    // Only send notification if user is in range and has a valid FCM token
    if (!inRange || !user.fcm_token) {
        return;
    }

    const title = '🍽️  New Meal Planned!';
    // Ensure mealType is a string before calling toUpperCase
    const body = `${String(mealType)[0].toUpperCase()}${String(mealType).slice(1)} at ${mealTime}. Will you join?`;

    const payload = {
      notification: {
        title,
        body,
        click_action: 'FLUTTER_NOTIFICATION_CLICK', // For Android
      },
      data: {
        mealId: event.params.mealId,
        type: mealType,
        mealTime,
      },
      apns: { // APNS config for iOS click action
        payload: {
          aps: {
            'click_action': 'FLUTTER_NOTIFICATION_CLICK',
          },
        },
      },
      token: user.fcm_token, // In v2, it's often cleaner to send one by one
    };
    
    // Using send() instead of sendToDevice for clarity, though both can work
    notificationPromises.push(admin.messaging().send(payload));
  });

  // Wait for all notification sending jobs to complete
  await Promise.all(notificationPromises);
  console.log(`Notifications sent for meal ${event.params.mealId}`);
});
