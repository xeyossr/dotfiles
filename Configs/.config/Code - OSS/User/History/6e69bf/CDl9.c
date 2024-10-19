#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/utsname.h>
#include <pwd.h>
#include <dirent.h>
#include <time.h>

#define IMAGE_VIEWER "w3m" // w3m aracını kullanarak terminalde görüntüleme

// Renk tanımları (ANSI kodları)
#define RED "\033[0;31m"
#define GREEN "\033[0;32m"
#define YELLOW "\033[0;33m"
#define BLUE "\033[0;34m"
#define RESET "\033[0m"

// Rastgele bir piksel art seçmek için
void print_random_pixel_art(const char *folder) {
    struct dirent *entry;
    DIR *dp = opendir(folder);
    
    if (dp == NULL) {
        perror("PNG klasörü açılamadı.");
        return;
    }

    // Klasördeki PNG dosyalarını say
    int count = 0;
    while ((entry = readdir(dp)) != NULL) {
        if (strstr(entry->d_name, ".png")) { // Yalnızca PNG dosyalarını al
            count++;
        }
    }

    if (count == 0) {
        printf("PNG bulunamadı.\n");
        closedir(dp);
        return;
    }

    // Rastgele bir dosya seç
    srand(time(NULL));
    int random_index = rand() % count;

    rewinddir(dp);
    count = 0;
    while ((entry = readdir(dp)) != NULL) {
        if (strstr(entry->d_name, ".png")) {
            if (count == random_index) {
                char path[256];
                snprintf(path, sizeof(path), "%s/%s", folder, entry->d_name);
                
                // w3m ile PNG dosyasını terminalde göster
                char command[512];
                snprintf(command, sizeof(command), "echo -e '0;1;1;1;400;400;;;;;%s\n4;' | %s", path, IMAGE_VIEWER);
                system(command);
                break;
            }
            count++;
        }
    }

    closedir(dp);
}

// Kullanıcı adı ve hostname al
void print_username_and_hostname() {
    char hostname[1024];
    gethostname(hostname, 1024);

    struct passwd *pw;
    pw = getpwuid(getuid());

    printf(GREEN "%s" RESET "@" BLUE "%s\n" RESET, pw->pw_name, hostname);
}

// OS bilgisi
void print_os() {
    printf(YELLOW "OS: " RESET);
    // /etc/os-release dosyasından bilgi al
    FILE *os_release = fopen("/etc/os-release", "r");
    if (os_release) {
        char line[256];
        while (fgets(line, sizeof(line), os_release)) {
            if (strncmp(line, "PRETTY_NAME", 11) == 0) {
                char *os_name = strchr(line, '=');
                if (os_name) {
                    os_name++; // '=' işaretinden sonrasını al
                    os_name[strlen(os_name) - 1] = '\0'; // Yeni satırı kaldır
                    printf("%s\n", os_name);
                }
                break;
            }
        }
        fclose(os_release);
    } else {
        printf("Bilinmiyor\n");
    }
}

// Kernel bilgisi
void print_kernel() {
    struct utsname buffer;
    if (uname(&buffer) == 0) {
        printf(YELLOW "Kernel: " RESET "%s\n", buffer.release);
    }
}

// Paket sayısı (pacman için örnek)
void print_package_count() {
    printf(YELLOW "Packages: " RESET);
    FILE *packages = popen("pacman -Q | wc -l", "r");
    if (packages) {
        char line[10];
        if (fgets(line, sizeof(line), packages)) {
            printf("%s", line);
        }
        pclose(packages);
    }
}

// Display bilgisi
void print_display() {
    printf(YELLOW "Display: " RESET);
    char *display = getenv("DISPLAY");
    if (display) {
        printf("%s\n", display);
    } else {
        printf("N/A\n");
    }
}

// WM/DE bilgisi
void print_wm_de() {
    printf(YELLOW "WM/DE: " RESET);
    char *wm_de = getenv("XDG_CURRENT_DESKTOP");
    if (wm_de) {
        printf("%s\n", wm_de);
    } else {
        printf("N/A\n");
    }
}

// Uptime
void print_uptime() {
    printf(YELLOW "Uptime: " RESET);
    FILE *uptime = fopen("/proc/uptime", "r");
    if (uptime) {
        double up_seconds;
        if (fscanf(uptime, "%lf", &up_seconds)) {
            int hours = (int)up_seconds / 3600;
            int minutes = ((int)up_seconds % 3600) / 60;
            printf("%d saat %d dakika\n", hours, minutes);
        }
        fclose(uptime);
    }
}

int main() {
    // Piksel art klasörünü buraya koyun
    const char *pixel_art_folder = "./pixel_arts";

    // Piksel artı yazdır
    print_random_pixel_art(pixel_art_folder);

    // Sistem bilgilerini yazdır
    print_username_and_hostname();
    print_os();
    print_kernel();
    print_package_count();
    print_display();
    print_wm_de();
    print_uptime();

    return 0;
}
