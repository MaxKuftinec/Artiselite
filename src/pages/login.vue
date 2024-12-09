<template>
  <v-container class="d-flex justify-center align-center fill-height">
    <v-card class="pa-4" width="400">
      <v-card-title class="text-h5 justify-center">Login</v-card-title>
      <v-card-text>
        <v-form ref="loginForm" @submit.prevent="handleLogin" v-model="valid">
          <v-text-field
            label="Username"
            v-model="username"
            :rules="[rules.required]"
            outlined
            dense
          ></v-text-field>
          <v-text-field
            label="Password"
            v-model="password"
            :rules="[rules.required]"
            type="password"
            outlined
            dense
          ></v-text-field>
					<!-- Error message -->
					<div v-if="errorMessage" class="error-text mt-2">{{ errorMessage }}</div>
          <v-btn
            :disabled="!valid"
            class="mt-4"
            color="primary"
            block
            type="submit"
          >
            Login
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { useUserStore } from '@/stores/users';

export default {
  data() {
    return {
      username: "",
      password: "",
      valid: false,
			errorMessage: "", // Error message to display if login fails
      rules: {
        required: (value) => !!value || "This field is required.",
      },
    };
  },
  methods: {
    async handleLogin() {
			const userStore = useUserStore();
			this.errorMessage = ""; // Clear any existing error message
      if (!this.valid) return;

      const loginPayload = {
        username: this.username,
        password: this.password,
      };

			try {
				await userStore.login(loginPayload.username, loginPayload.password);
				console.log('Login successful');
				this.$router.push("/");
			}
			catch (error) {
				console.error(error);
				this.errorMessage = error.message;
			}
    }
  },
};
</script>

<style scoped>
.fill-height {
  height: 100vh;
}

.error-text {
  color: red;
	font-size: 0.9rem;
}
</style>
