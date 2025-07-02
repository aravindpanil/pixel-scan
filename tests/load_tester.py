from locust import HttpUser, task, between

class UploadUser(HttpUser):
    
    # Launch new requests for each user between 1 and 2 seconds
    wait_time = between(1, 2)

    @task
    def upload_image(self):
        
        # Open an image from Sample n number of times as defined in locus configuration
        with open("samples/Coffee.jpg", "rb") as f:
            files = {
                "image": ("Coffee.jpg", f, "image/jpeg")
            }
            response = self.client.post("/", files=files)
