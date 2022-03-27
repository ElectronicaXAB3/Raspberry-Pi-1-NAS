### Implement NodeJS like signal processing in Python

```text
// If ctrl+c is hit, free resources and exit.
process.on('SIGINT', shutdown_ctrl_c);
// If ctrl+z is hit, free resources and exit.
process.on('SIGTSTP', shutdown_ctrl_z);
// If kill signal, free resources and exit.
// process.on('SIGKILL', shutdown);
// If kill signal, free resources and exit.
process.on('SIGTERM', shutdown); 
```
