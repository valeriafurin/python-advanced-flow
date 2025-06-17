const payButton = document.getElementById("loadPaymentMethods")

const dropdown = document.getElementById("countries");
console.log(dropdown.value); // Logs the initially selected value (e.g., "DE")

// Add an event listener to detect changes
dropdown.addEventListener("change", function() {
    console.log(this.value); // Logs the new selected value when changed
});

// const clientKey = document.getElementById("client-key").innerHTML();
const clientKey = "test_TX647WMLYBCOLKDZUVLN3Y6XYQ3LTF46"
const { AdyenCheckout, Card } = window.AdyenWeb;
payButton.addEventListener('click', startCheckout);

// Used to finalize a checkout call in case of redirect
const urlParams = new URLSearchParams(window.location.search);
const sessionId = urlParams.get('sessionId'); // Unique identifier for the payment session
const redirectResult = urlParams.get('redirectResult');

async function handleRedirect() {
  const urlParams = new URLSearchParams(window.location.search);
  const redirectResult = urlParams.get("redirectResult");

  if (redirectResult) {
    try {
      const response = await fetch(`/api/handleShopperRedirect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ redirectResult }),
      });

      const result = await response.json();

      if (result.resultCode === "Authorised") {
        window.location.href = "/result/success";
      } else if (result.resultCode === "Pending" || result.resultCode === "Received") {
        window.location.href = "/result/pending";
      } else {
        window.location.href = "/result/error";
      }
    } catch (error) {
      console.error("Error handling redirect:", error);
      window.location.href = "/result/error";
    }
  }
}

// Run handleRedirect when the page loads
handleRedirect();

async function startCheckout() {
  try {
    const paymentMethodsResponse = await fetch('/api/paymentMethods', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }, 
      body: JSON.stringify({"countryCode": dropdown.value}),
    }).then(response => response.json());

    const configuration = {
      paymentMethodsResponse: paymentMethodsResponse,
      // showPayButton: false,
      clientKey,
      environment: "test",
      amount: {
        value: 1230,
        currency: 'EUR'
      },
      locale: "en_US",
      countryCode: dropdown.value,
      showPayButton: true,
      // override Security Code label
      translations: {
        'en-US': {
          'creditCard.securityCode.label': 'CVV/CVC'
        }
      },
      onSubmit: async (state, component, actions) => {
        console.info("onSubmit", state, component, actions);
        try {
          if (state.isValid) {
            const {resultCode, action, order} = await fetch("/api/payments", {
              method: "POST",
              body: state.data ? JSON.stringify(state.data) : "",
              headers: {
                "Content-Type": "application/json",
              }
            }).then(response => response.json());
            // console.log("response:", response);
            

            if (!resultCode) {
              console.warn("reject");
              actions.reject();
            }

            actions.resolve({
              resultCode,
              action,
              order
            });
          }
        } catch (error) {
          console.error(error);
          actions.reject();
        }
      },
      onPaymentCompleted: (result, component) => {
        console.info("onPaymentCompleted", result, component);
        // handleOnPaymentCompleted(result.resultCode);
      },
      onPaymentFailed: (result, component) => {
        console.info("onPaymentFailed", result, component);
        // handleOnPaymentFailed(result.resultCode);
      },
      onError: (error, component) => {
        console.error("onError", error.name, error.message, error.stack, component);
        window.location.href = "/result/error";
      },
      // Used for the Native 3DS2 Authentication flow, see: https://docs.adyen.com/online-payments/3d-secure/native-3ds2/
      onAdditionalDetails: async (state, component, actions) => {
        console.info("onAdditionalDetails", state, component);
        try {
          const { resultCode } = await fetch("/api/payments/details", {
            method: "POST",
            body: state.data ? JSON.stringify(state.data) : "",
            headers: {
              "Content-Type": "application/json",
            }
          }).then(response => response.json());

          if (!resultCode) {
            console.warn("reject");
            actions.reject();
          }

          actions.resolve({ resultCode });
        } catch (error) {
          console.error(error);
          actions.reject();
        }
      }
    };

    const blockedBins = ['411111']

    const paymentMethodsConfiguration = {
      storedCard: {
        hideCVC: true,
        // styles: //your styles for stored cards
      },

      card: {
        billingAddressRequired: true,
        showBrandIcon: true,
        hasHolderName: true,
        holderNameRequired: true,
        name: "Credit or debit card",
        enableStoreDetails: true,
        onBinLookup: (state) => {
          console.log("onBinLookup", state);
        },
        onBinValue: (state) => {
          // if (blockedBins.includes(state.binValue)) {
          //   alert("BIN NOT ALLOWED")
          // }
          console.log("onBinValue", state);
        },
        onFieldValid: (state) => {
          console.log("onFieldValid", state);
        },
        // amount: {
        //   value: 10000,
        //   currency: "EUR",
        // },
        placeholders: {
          cardNumber: '1234 5678 9012 3456',
          expiryDate: 'MM/YY',
          securityCodeThreeDigits: '123',
          securityCodeFourDigits: '1234',
          holderName: 'J. Smith'
        }
      }
    };

    const paypalConfiguration = {
      intent: "authorize"
  };

    // Start the AdyenCheckout and mount the element onto the 'payment' div.
    const adyenCheckout = await AdyenCheckout(configuration, paypalConfiguration);
    const card = new Card(adyenCheckout, {
      paymentMethodsConfiguration: paymentMethodsConfiguration
    }).mount('#component-container');

  } catch (error) {
    console.error(error);
    alert("Error occurred. Look at console for details.");
  }
}

// Function to handle payment completion redirects
function handleOnPaymentCompleted(resultCode) {
  switch (resultCode) {
    case "Authorised":
      console.log("Success!", resultCode);

      // window.location.href = "/result/success";
      
      break;
    case "Pending":
    case "Received":
      window.location.href = "/result/pending";
      break;
    default:
      window.location.href = "/result/error";
      break;
  }
}

// Function to handle payment failure redirects
function handleOnPaymentFailed(resultCode) {
  switch (resultCode) {
    case "Cancelled":
    case "Refused":
      window.location.href = "/result/failed";
      break;
    default:
      window.location.href = "/result/error";
      break;
  }
}

// startCheckout();


