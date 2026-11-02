import com.stripe.Stripe;
import com.stripe.exception.SignatureVerificationException;
import com.stripe.model.Event;
import com.stripe.model.EventDataObjectDeserializer;
import com.stripe.model.PaymentIntent;
import com.stripe.model.StripeObject;
import com.stripe.model.checkout.Session;
import com.stripe.net.Webhook;
import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

import static spark.Spark.*;

public class App {
    private static Gson gson = new Gson();

    public static void main(String[] args) {
        // Atur port server lokal
        port(4242);

        // 1. Masukkan Secret Key Stripe Anda (Gunakan test key untuk pengembangan)
        Stripe.apiKey = "sk_test_4eC39HqLyjWDarjtT1zdp7dc";

        // Endpoint untuk membuat Sesi Checkout Produk
        post("/create-checkout-session", (req, res) -> {
            res.type("application/json");
            
            // Konfigurasi parameter Sesi Checkout
            com.stripe.param.checkout.SessionCreateParams params = 
                com.stripe.param.checkout.SessionCreateParams.builder()
                    .setMode(com.stripe.param.checkout.SessionCreateParams.Mode.PAYMENT)
                    .setSuccessUrl("https://example.com/success.html")
                    .setCancelUrl("https://example.com/cancel.html")
                    .addLineItem(
                        com.stripe.param.checkout.SessionCreateParams.LineItem.builder()
                            .setQuantity(1L)
                            .setPriceData(
                                com.stripe.param.checkout.SessionCreateParams.LineItem.PriceData.builder()
                                    .setCurrency("usd")
                                    .setUnitAmount(4242L) // Harga dalam sen (contoh: $42.42)
                                    .setProductData(
                                        com.stripe.param.checkout.SessionCreateParams.LineItem.PriceData.ProductData.builder()
                                            .setName("Produk Contoh Stripe")
                                            .build()
                                    )
                                    .build()
                            )
                            .build()
                    )
                    .build();

            Session session = Session.create(params);
            res.status(200);
            return gson.toJson(new CheckoutResponse(session.getUrl()));
        });

        // 2. Endpoint Webhook untuk Menerima Kejadian dari Stripe
        post("/stripe_webhooks", (request, response) -> {
            String payload = request.body();
            String sigHeader = request.headers("Stripe-Signature");
            
            // Rahasia endpoint webhook dari Dashboard atau Stripe CLI (whsec_...)
            String endpointSecret = "whsec_..." ; 

            Event event = null;

            try {
                // Verifikasi tanda tangan webhook (Praktik Terbaik Keamanan)
                event = Webhook.constructEvent(payload, sigHeader, endpointSecret);
            } catch (JsonSyntaxException e) {
                // Payload tidak valid (JSON error)
                response.status(400);
                return "";
            } catch (SignatureVerificationException e) {
                // Tanda tangan tidak valid (potensi serangan atau secret salah)
                response.status(400);
                return "";
            }

            // Deserialisasi objek di dalam event
            EventDataObjectDeserializer dataObjectDeserializer = event.getDataObjectDeserializer();
            StripeObject stripeObject = null;
            if (dataObjectDeserializer.getObject().isPresent()) {
                stripeObject = dataObjectDeserializer.getObject().get();
            } else {
                // Deserialisasi gagal karena ketidakcocokan versi API
                response.status(400);
                return "";
            }

            // Tangani tipe kejadian (Event Type) sesuai kebutuhan bisnis
            switch (event.getType()) {
                case "payment_intent.succeeded":
                    PaymentIntent paymentIntent = (PaymentIntent) stripeObject;
                    System.out.println("Pembayaran Berhasil untuk PaymentIntent ID: " + paymentIntent.getId());
                    // TODO: Lakukan aksi backend (ubah status database, kirim email, dll)
                    break;

                case "checkout.session.completed":
                    com.stripe.model.checkout.Session session = (com.stripe.model.checkout.Session) stripeObject;
                    System.out.println("Checkout Session Selesai: " + session.getId());
                    // TODO: Berikan akses produk ke pelanggan
                    break;

                default:
                    System.out.println("Tipe kejadian tidak ditangani: " + event.getType());
                    break;
            }

            // Segera kembalikan status 200 OK ke Stripe
            response.status(200);
            return "";
        });
    }

    // Helper class untuk response JSON checkout
    private static class CheckoutResponse {
        private String url;
        public CheckoutResponse(String url) { this.url = url; }
    }
}
// Tambahkan di dalam public static void main(String[] args) sebelum endpoint dibuat:
options("/*", (request, response) -> {
    String accessControlRequestHeaders = request.headers("Access-Control-Request-Headers");
    if (accessControlRequestHeaders != null) {
        response.header("Access-Control-Allow-Headers", accessControlRequestHeaders);
    }
    String accessControlRequestMethod = request.headers("Access-Control-Request-Method");
    if (accessControlRequestMethod != null) {
        response.header("Access-Control-Allow-Methods", accessControlRequestMethod);
    }
    return "OK";
});

before((request, response) -> {
    response.header("Access-Control-Allow-Origin", "*");
    response.header("Access-Control-Allow-Credentials", "true");
});
