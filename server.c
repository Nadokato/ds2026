#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
    char buffer[BUFFER_SIZE];
    int bytes_read;

    // Create socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    // Setup address
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Bind
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d...\n", PORT);

    // Accept
    new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen);
    if (new_socket < 0) {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }

    // Read file name
    memset(buffer, 0, BUFFER_SIZE);
    read(new_socket, buffer, BUFFER_SIZE);
    printf("Receiving file: %s\n", buffer);

    FILE *fp = fopen(buffer, "wb");
    if (fp == NULL) {
        perror("File open error");
        exit(1);
    }

    // Receive file data
    while ((bytes_read = recv(new_socket, buffer, BUFFER_SIZE, 0)) > 0) {
        fwrite(buffer, 1, bytes_read, fp);
    }

    printf("File received successfully!\n");

    fclose(fp);
    close(new_socket);
    close(server_fd);
    return 0;
}
