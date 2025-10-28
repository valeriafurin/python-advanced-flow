// === DOM ELEMENTS ===
const resultTemplate = document.querySelector(".auth-result");
const resultMessage = document.querySelector("p.auth-result-msg");
const payButton = document.getElementById("loadPaymentMethods");
const countryDropdown = document.getElementById("countries");

// === CONSTANTS ===
const clientKey = "test_TX647WMLYBCOLKDZUVLN3Y6XYQ3LTF46";
const {
  AdyenCheckout,
  Dropin,
  SepaDirectDebit,
  Klarna,
  RatePay,
  OnlineBankingPL,
} = window.AdyenWeb;

// === UTILITIES ===
const renderResultTemplate = (message) => {
  resultMessage.innerHTML = `${message}`;
  resultTemplate.classList.add("show-auth-result");
};

const fetchWithTimeout = (url, options, timeout = 5000) =>
  Promise.race([
    fetch(url, options),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error("Request timed out")), timeout)
    ),
  ]);

payButton.addEventListener("click", startCheckout);

// === MAIN FUNCTION: Checkout Setup ===
async function startCheckout() {
  try {
    const selectedCountry = countryDropdown.value;
    const selectedCurrency =
      countryDropdown.options[countryDropdown.selectedIndex].getAttribute(
        "data-currency"
      );

    const paymentMethodsResponse = await fetch("/api/paymentMethods", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        countryCode: selectedCountry,
        currency: selectedCurrency,
      }),
    }).then((res) => res.json());

    const checkout = await AdyenCheckout({
      paymentMethodsResponse,
      clientKey,
      environment: "test",
      countryCode: selectedCountry,
      locale: "en_US",
      amount: { value: 5995, currency: selectedCurrency },
      showPayButton: true,
      translations: {
        "en-US": {
          "creditCard.securityCode.label": "CVV/CVC",
        },
      },
      onSubmit: handleSubmit,
      onPaymentCompleted: (result) =>
        handleOnPaymentCompleted(result.resultCode),
      onPaymentFailed: (result) => handleOnPaymentFailed(result.resultCode),
      onChange: (state) => console.log("onChange:", state),
      onError: handleError,
      onAdditionalDetails: handleAdditionalDetails,
    });

    const dropin = new Dropin(checkout, dropinConfiguration());

    dropin.mount("#dropin-container");
  } catch (error) {
    console.error("Checkout Error:", error);
    alert("An error occurred. See console for details.");
  }
}

// === HANDLERS ===
async function handleSubmit(state, component, actions) {
  console.info("onSubmit", JSON.stringify(state));
  try {
    if (state.isValid) {
      const selectedCountry = countryDropdown.value;
      const selectedCurrency =
        countryDropdown.options[countryDropdown.selectedIndex].getAttribute(
          "data-currency"
        );
      state.countryCode = selectedCountry;
      state.amount = { currency: selectedCurrency, value: 5995 };
      state.paymentMethod = state.data.paymentMethod;

      const payload = {
        ...state,
      };

      console.log("payload", payload);

      const { action, order, resultCode } = await fetch("/api/payments", {
        method: "POST",
        // body: state.data ? JSON.stringify(state.data) : "",
        body: JSON.stringify(payload),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => response.json());

      if (!resultCode) {
        console.warn("reject");
        actions.reject();
      }

      actions.resolve({
        resultCode,
        action,
        order,
      });
    }
  } catch (error) {
    console.error(error);
    actions.reject();
  }
}

async function handleAdditionalDetails(state, component, actions) {
  try {
    const response = await fetchWithTimeout("/api/payments/details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state.data),
    });

    if (!response.ok) throw new Error(`Status: ${response.status}`);

    const { resultCode } = await response.json();

    if (!resultCode) {
      actions.reject();
    } else {
      actions.resolve({ resultCode });
    }
  } catch (error) {
    console.error("Additional Details Error:", error);
    actions.reject();
  }
}

function handleError(error) {
  console.error("Checkout Error:", error);
  window.location.href = "/error";
}

function handleOnPaymentCompleted(resultCode) {
  switch (resultCode) {
    case "Authorised":
      window.location.href = "/success";
      break;
    case "Pending":
    case "Received":
      window.location.href = "/pending";
      break;
    default:
      window.location.href = "/error";
  }
}

function handleOnPaymentFailed(resultCode) {
  switch (resultCode) {
    case "Cancelled":
    case "Refused":
      window.location.href = "/failed";
      break;
    default:
      window.location.href = "/error";
  }
}

// === PAYMENT CONFIGURATION ===
function dropinConfiguration() {
  return {
    paymentMethodsConfiguration: {
      paypal: {
        merchantId: "L89RAC3HBQU9G",
        intent: "capture",
      },
      storedCard: {
        hideCVC: false,
      },
      showStoredPaymentMethods: true,
      card: {
        clickToPayConfiguration: {
          merchantDisplayName: "TestCompany_ValeriaFurinUC_TEST",
          shopperEmail: "valeria.furin@adyen.com",
        },
        billingAddressRequired: false,
        showBrandIcon: true,
        hasHolderName: true,
        holderNameRequired: false,
        name: "Credit or debit card",
        enableStoreDetails: true,
        showStorePaymentField: true,
        placeholders: {
          cardNumber: "1234 5678 9012 3456",
          expiryDate: "MM/YY",
          securityCodeThreeDigits: "123",
          securityCodeFourDigits: "1234",
          holderName: "J. Smith",
        },
        onBinLookup: (state) => console.log("onBinLookup", state),
        onBinValue: (state) => console.log("onBinValue", state),
        onFieldValid: (state) => console.log("onFieldValid", state),
      },
    },
  };
}

// === REDIRECT HANDLING ===
async function handleRedirect() {
  const params = new URLSearchParams(window.location.search);
  const redirectResult = params.get("redirectResult");

  if (!redirectResult) return;

  try {
    const response = await fetch("/api/handleShopperRedirect", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ redirectResult }),
    });

    const { resultCode } = await response.json();

    switch (resultCode) {
      case "Authorised":
        window.location.href = "/success";
        break;
      case "Pending":
      case "Received":
        window.location.href = "/pending";
        break;
      default:
        window.location.href = "/error";
    }
  } catch (error) {
    console.error("Redirect Handling Error:", error);
    window.location.href = "/error";
  }
}

// === INIT ON LOAD ===
window.onload = handleRedirect;
