# vpc/main.tf

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr           # Główny zakres adresów IP dla VPC
  enable_dns_support   = true                   # Obsługa DNS wewnątrz VPC
  enable_dns_hostnames = true                   # Automatyczne przypisywanie publicznych nazw DNS hostom z publicznymi IP

  tags = {
    Name = var.vpc_name
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id                      # Brama internetowa do utworzonej VPC

  tags = {
    Name = "${var.vpc_name}-igw"
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id                      # Podsieć należy do głównej VPC
  cidr_block              = var.subnet_cidrs["public_a"]         # Zakres adresów IP dla podsieci publicznej A
  availability_zone       = var.availability_zones["public_a"]   # Strefa dostępności dla podsieci A
  map_public_ip_on_launch = true                                 # Przypisanie publicznego IP instancjom w podsieci

  tags = {
    Name = "${var.vpc_name}-public-a"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.main.id                      # Podsieć należy do głównej VPC
  cidr_block              = var.subnet_cidrs["public_b"]         # Zakres adresów IP dla podsieci publicznej B
  availability_zone       = var.availability_zones["public_b"]   # Strefa dostępności dla podsieci B
  map_public_ip_on_launch = true                                 # Przypisanie publicznego IP instancjom w podsieci

  tags = {
    Name = "${var.vpc_name}-public-b"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id                      # Tablica routingu należy do głównej VPC

  tags = {
    Name = "${var.vpc_name}-public-rt"
  }
}

resource "aws_route" "default" {
  route_table_id         = aws_route_table.public.id    # Trasa należy do publicznej tablicy routingu
  destination_cidr_block = "0.0.0.0/0"                  # Trasa domyślna dla całego ruchu wychodzącego do internetu
  gateway_id             = aws_internet_gateway.main.id # Kierowanie ruchu przez bramę internetową
}

resource "aws_route_table_association" "public_a" {
  # Połączenie podsieci publicznej A z tablicą routingu
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  # Połączenie podsieci publicznej B z tablicą routingu
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "all_open" {
  name        = "${var.vpc_name}-sg-all-open"     # Nazwa grupy bezpieczeństwa
  description = "Allow all inbound and outbound traffic" # Opis grupy bezpieczeństwa
  vpc_id      = aws_vpc.main.id                   # Grupa bezpieczeństwa należy do głównej VPC

  ingress {                                       # Reguły ruchu przychodzącego
    from_port   = 0                               # Od portu 0
    to_port     = 0                               # Do portu 0 (oznacza wszystkie porty)
    protocol    = "-1"                            # Wszystkie protokoły
    cidr_blocks = ["0.0.0.0/0"]                   # Z dowolnego adresu IP
  }

  egress {                                        # Reguły ruchu wychodzącego
    from_port   = 0                               # Od portu 0
    to_port     = 0                               # Do portu 0 (oznacza wszystkie porty)
    protocol    = "-1"                            # Wszystkie protokoły
    cidr_blocks = ["0.0.0.0/0"]                   # Do dowolnego adresu IP
  }

  tags = {
    Name = "${var.vpc_name}-sg-all-open"
  }
}