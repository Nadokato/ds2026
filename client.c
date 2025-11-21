#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main(int argc, char *argv[]) {
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE];
    FILE *fp;
    int bytes_read;

    if (argc != 3) {
        printf("Usage: %s <server_ip> <file_name>\n", argv[0]);
        return 1;
    }

    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        printf("Socket creation error\n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Convert IP
    if (inet_pton(AF_INET, argv[1], &serv_addr.sin_addr) <= 0) {
        printf("Invalid address\n");
        return -1;
    }

    // Connect
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("Connection failed\n");
        return -1;
    }

    // Send file name
    send(sock, argv[2], strlen(argv[2]), 0);

    // Open file
    fp = fopen(argv[2], "rb");
    if (!fp) {
        printf("File not found\n");
        return 1;
    }

    // Send file data
    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, fp)) > 0) {
        send(sock, buffer, bytes_read, 0);
    }

    printf("File sent successfully.\n");

    fclose(fp);
    close(sock);
    return 0;
}
