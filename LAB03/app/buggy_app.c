#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_data(int *data, int len)
{
    int sum = 0;

    // BUG 1: Truy cap vuot gioi han mang
    for (int i = 0; i <= len; i++) {
        sum += data[i];
    }

    printf("Sum = %d\n", sum);
}

char *create_message(const char *text)
{
    char *buf = malloc(strlen(text) + 1);

    if (buf == NULL) {
        return NULL;
    }

    strcpy(buf, text);

    // BUG 2: Su dung con tro sau khi giai phong bo nho
    free(buf);

    return buf;
}

int calculate(int a, int b)
{
    // BUG 3: Co the tran so nguyen co dau
    int result = a * b;

    printf("Result = %d\n", result);

    return result;
}

int main(void)
{
    int arr[5] = {1, 2, 3, 4, 5};

    printf("Starting buggy application...\n");

    process_data(arr, 5);

    char *msg = create_message("Hello Embedded Linux");

    if (msg != NULL) {
        printf("Message: %s\n", msg);
    }

    calculate(100000, 100000);

    printf("Application finished.\n");

    return 0;
}
