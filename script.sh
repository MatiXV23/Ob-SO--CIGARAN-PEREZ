#!/bin/bash

configurar_contaduria() {
    echo "Configurando perfil de Contaduría..."
    USER="contaduria"
    PASSWORD="passwordContaduria" 

   
    if ! id "$USER" &>/dev/null; then
        sudo useradd -m -s /bin/bash "$USER"
        echo "$USER:$PASSWORD" | sudo chpasswd
        echo "Usuario '$USER' creado."
    else
        echo "Usuario '$USER' ya existe."
    fi

    
    DESKTOP_DIR="/home/$USER/Escritorio"
    ACCOUNTING_DIR="$DESKTOP_DIR/Asientos"
    sudo -u "$USER" mkdir -p "$ACCOUNTING_DIR"
    sudo -u "$USER" mkdir -p "$ACCOUNTING_DIR/Diario"
    sudo -u "$USER" mkdir -p "$ACCOUNTING_DIR/Semanal"
    sudo -u "$USER" mkdir -p "$ACCOUNTING_DIR/Mensual"
    echo "Carpetas 'Asientos/Diario', 'Asientos/Semanal', 'Asientos/Mensual' creadas para '$USER'."

   
    BACKUP_ROOT="/Respaldo"
    CURRENT_DATE=$(date +"%d%b%Y" | tr '[:lower:]' '[:upper:]') 
    DEST_BACKUP_DIR="$BACKUP_ROOT/$CURRENT_DATE"

    sudo mkdir -p "$DEST_BACKUP_DIR"
    echo "Carpeta de respaldo '$DEST_BACKUP_DIR' creada."


    sudo rsync -av --exclude '.*' "$ACCOUNTING_DIR/" "$DEST_BACKUP_DIR/"
    echo "Respaldo de 'Asientos' realizado en '$DEST_BACKUP_DIR'."       
    echo "Restricciones de instalación para '$USER' (requiere configuración manual de sudoers)."
    echo "Acceso a otras carpetas de usuarios restringido por defecto en Linux."
    echo "Perfil de Contaduría configurado."
    echo ""
}


configurar_soporte() {
    echo "Configurando perfil de Soporte..."
    USER="soporte"
    PASSWORD="passwordSoporte" 


    if ! id "$USER" &>/dev/null; then
        sudo useradd -m -s /bin/bash "$USER"
        echo "$USER:$PASSWORD" | sudo chpasswd
        echo "Usuario '$USER' creado."
    else
        echo "Usuario '$USER' ya existe."
    fi

    sudo usermod -aG sudo "$USER" 
    echo "Usuario '$USER' añadido al grupo 'sudo' para permisos elevados."

   
    echo "Perfil de Soporte configurado (acceso completo y capacidad de instalación)."
    echo ""
}

# Función para configurar el perfil de Relaciones Públicas
configurar_rrpp() {
    echo "Configurando perfil de Relaciones Publicas..."
    USER="rrpp"
    PASSWORD="passwordRrpp"


    if ! id "$USER" &>/dev/null; then
        sudo useradd -m -s /bin/bash "$USER"
        echo "$USER:$PASSWORD" | sudo chpasswd
        echo "Usuario '$USER' creado."
    else
        echo "Usuario '$USER' ya existe."
    fi

    DESKTOP_DIR="/home/$USER/Escritorio"
    COMUNICADOS_DIR="$DESKTOP_DIR/Comunicados"
    sudo -u "$USER" mkdir -p "$COMUNICADOS_DIR"
    sudo -u "$USER" mkdir -p "$COMUNICADOS_DIR/Semanal"
    sudo -u "$USER" mkdir -p "$COMUNICADOS_DIR/Mensual"
    echo "Carpetas 'Comunicados/Semanal', 'Comunicados/Mensual' creadas para '$USER'."


    BACKUP_ROOT="/Respaldo"
    CURRENT_DATE=$(date +"%d%b%Y" | tr '[:lower:]' '[:upper:]') 
    DEST_BACKUP_DIR="$BACKUP_ROOT/$CURRENT_DATE"

    sudo mkdir -p "$DEST_BACKUP_DIR"
    echo "Carpeta de respaldo '$DEST_BACKUP_DIR' creada."


    sudo rsync -av --exclude '.*' "$COMUNICADOS_DIR/" "$DEST_BACKUP_DIR/"
    echo "Respaldo de 'Comunicados' realizado en '$DEST_BACKUP_DIR'."

    echo "Restricciones de instalación para '$USER' (requiere configuración manual de sudoers)."
    echo "Acceso a otras carpetas de usuarios restringido por defecto en Linux."
    echo "Perfil de Relaciones Publicas configurado."
    echo ""
}


configurar_recepcion() {
    echo "Configurando perfil de Recepción..."
    USER="recepcion"
    PASSWORD="passwordRecepcion" 


    if ! id "$USER" &>/dev/null; then
        sudo useradd -m -s /bin/bash "$USER"
        echo "$USER:$PASSWORD" | sudo chpasswd
        echo "Usuario '$USER' creado."
    else
        echo "Usuario '$USER' ya existe."
    fi


    sudo chmod 700 "/home/$USER"
    sudo chown "$USER":"$USER" "/home/$USER"
    echo "Permisos de directorio home de '$USER' configurados para acceso restringido."
    echo "Restricción de ejecución de navegadores requiere configuración manual."
    echo "Perfil de Recepción configurado."
    echo ""
}



echo "Iniciando configuración de perfiles de usuario..."
echo "---"

configurar_contaduria
configurar_soporte
configurar_rrpp
configurar_recepcion

echo "---"
echo "Configuración de perfiles completada. Revise la sección de configuración manual para finalizar."