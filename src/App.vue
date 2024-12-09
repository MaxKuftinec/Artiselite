<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useUserStore } from './stores/users';
import axios from 'axios';

const userStore = useUserStore(); // Get the store instance

const token = localStorage.getItem('token');
if (token) {
  userStore.token = token; // Access and modify the store
  axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  userStore.isAuthenticated = true;
}
else
  userStore.isAuthenticated = false;
</script>
