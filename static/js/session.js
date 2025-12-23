// === DOM ELEMENTS ===
const resultTemplate = document.querySelector(".auth-result");
const resultMessage = document.querySelector("p.auth-result-msg");
const payButton = document.getElementById("loadPaymentMethods");
const countryDropdown = document.getElementById("countries");

// === CONSTANTS ===
// Note: clientKey should be your real key or passed via a config
const clientKey = "test_TX647WMLYBCOLKDZUVLN3Y6XYQ3LTF46"; 
const { AdyenCheckout, Dropin } = window.AdyenWeb;

// === EVENT LISTENERS ===
payButton.addEventListener("click", startCheckout);

// === MAIN FUNCTION: Sessions Flow ===
async function startCheckout() {
  try {
    const selectedCountry = countryDropdown.value;
    const selectedCurrency = countryDropdown.options[countryDropdown.selectedIndex].getAttribute("data-currency");

    // 1. Create the session on your backend
    const sessionResponse = await fetch("/api/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        countryCode: selectedCountry,
        amount: { value: 5995, currency: selectedCurrency }, // e.g., €59.95
        returnUrl: window.location.href // Adyen will redirect back here
      }),
    });

    const session = await sessionResponse.json();

    // 2. Initialize AdyenCheckout with the session object
    const checkout = await AdyenCheckout({
      environment: "test",
      clientKey: clientKey,
      session: {
        id: session.id,
        sessionData: session.sessionData
      },
      onPaymentCompleted: (result, component) => {
        handleFinalResult(result.resultCode);
      },
      onError: (error, component) => {
        console.error(error.name, error.message);
      },
      // Optional: configuration for specific payment methods
      paymentMethodsConfiguration: dropinConfiguration().paymentMethodsConfiguration
    });

    // 3. Create and mount Drop-in
    const dropin = new Dropin(checkout);
    dropin.mount("#dropin-container");

  } catch (error) {
    console.error("Checkout Error:", error);
    alert("Could not initialize checkout session.");
  }
}

// === UTILITIES / CONFIG ===
function handleFinalResult(resultCode) {
  switch (resultCode) {
    case "Authorised":
      window.location.href = "/success";
      break;
    case "Pending":
    case "Received":
      window.location.href = "/pending";
      break;
    case "Refused":
      alert("Payment Refused.");
      break;
    default:
      window.location.href = "/error";
      break;
  }
}

function dropinConfiguration() {
  return {
    paymentMethodsConfiguration: {
      card: {
        hasHolderName: true,
        holderNameRequired: false,
        billingAddressRequired: false
      },
      paypal: {
        merchantId: "L89RAC3HBQU9G",
        intent: "authorize"
      }
    }
  };
}