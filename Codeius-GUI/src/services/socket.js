import io from 'socket.io-client';

const SOCKET_URL = 'http://localhost:8080';

class SocketService {
  constructor() {
    this.socket = null;
    this.listeners = {};
    this.connected = false;
  }

  connect() {
    if (this.socket?.connected) return;
    
    this.socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000
    });

    this.socket.on('connect', () => {
      console.log('✅ WebSocket connected');
      this.connected = true;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('❌ WebSocket disconnected:', reason);
      this.connected = false;
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
    });

    this.socket.on('reconnect', (attemptNumber) => {
      console.log(`🔄 WebSocket reconnected after ${attemptNumber} attempts`);
      this.connected = true;
    });

    this.socket.on('reconnect_attempt', () => {
      console.log('🔄 Attempting to reconnect...');
    });

    this.socket.on('reconnect_failed', () => {
      console.error('❌ Failed to reconnect');
    });
  }

  on(event, callback) {
    if (!this.socket) {
      console.warn('Socket not initialized. Call connect() first.');
      return;
    }
    
    this.socket.on(event, callback);
    this.listeners[event] = callback;
  }

  off(event) {
    if (this.socket && this.listeners[event]) {
      this.socket.off(event, this.listeners[event]);
      delete this.listeners[event];
    }
  }

  emit(event, data) {
    if (!this.socket) {
      console.error('Socket not initialized');
      return;
    }

    if (!this.connected) {
      console.warn('Socket not connected, event may not be sent');
    }

    this.socket.emit(event, data);
  }

  disconnect() {
    if (this.socket) {
      // Remove all listeners
      Object.keys(this.listeners).forEach(event => this.off(event));
      
      this.socket.disconnect();
      this.socket = null;
      this.connected = false;
    }
  }

  isConnected() {
    return this.connected && this.socket?.connected;
  }
}

// Export singleton instance
export default new SocketService();
