# RezUnitBot 🚀

A powerful and user-friendly Telegram bot for converting units across various categories, built with Python and pyTelegramBotAPI. Whether you're converting lengths 📏, weights ⚖️, or digital storage 💾, **UnitBot** makes it quick and easy right from any Telegram chat!

## ✨ Features

- **Wide Range of Units**: Supports conversions for length, weight, area, volume, time, temperature, speed, energy, pressure, angle, and digital storage.
- **Bilingual Support**: Provides help and start messages in both Persian 🇮🇷 and English 🇬🇧.
- **Emoji-Enhanced Output**: Clean and visually appealing results with category-specific emojis (e.g., 📏 for length, ⚡️ for energy).
- **Smart Number Formatting**:
  - Large numbers (≥ 100,000) formatted with commas (e.g., `10,000,000`).
  - Numbers ≥ 1,000 rounded to zero decimals (e.g., `10,000`).
  - Small numbers (< 1,000) shown with up to 2 decimal places (e.g., `6.21`).
  - Very small numbers (< 0.01) shown with up to 6 decimal places (e.g., `0.000006`).
- **Persian Number Support**: Accepts Persian numerals (e.g., `۱۰` or `۵.۵`) alongside English numbers.
- **Case-Insensitive Units**: Works with full unit names (e.g., `kilometer`) or abbreviations (e.g., `km`), regardless of case (e.g., `KM`, `KiLoMeTeR`).
- **Inline Mode**: Convert units directly in any Telegram chat using `@UnitBot <number> <unit>` (e.g., `@UnitBot 10 km`).
- **Error Logging**: Saves errors to `bot.log` for easy debugging.
- **New Units Added**: Includes `cc` (cubic centimeter) for volume and `petabyte` (PB), `exabyte` (EB) for digital storage.

## 📋 Supported Units

| Category       | Emoji | Units                                                                 |
|----------------|-------|----------------------------------------------------------------------|
| **Length**     | 📏    | millimeter (mm), centimeter (cm), meter (m), kilometer (km), decimeter (dm), inch (in), foot (ft), yard (yd), mile (mi) |
| **Weight**     | ⚖️    | milligram (mg), gram (g), kilogram (kg), ton (t), pound (lb)         |
| **Area**       | 🏞️    | centimeter square (cm2), meter square (m2), hectare (ha), inch square (in2), foot square (ft2), acre |
| **Volume**     | 🧴    | milliliter (ml), centimeter cubic (cm3), cc (cc), liter (l), meter cubic (m3), gallon (gal), barrel (bbl) |
| **Time**       | ⏱️    | second (s), minute (min), hour (h), day (d), week (wk), month (mo), year (yr) |
| **Temperature**| 🌡️   | celsius (C), fahrenheit (F), kelvin (K)                             |
| **Speed**      | 🚀    | meter per second (m/s), kilometer per hour (km/h), mile per hour (mph), mach |
| **Energy**     | ⚡️    | joule (J), kilojoule (kJ), megajoule (MJ), watt hour (Wh), kilowatt hour (kWh), calorie (cal), kilocalorie (kcal) |
| **Pressure**   | 🌬️    | pascal (Pa), kilopascal (kPa), atmosphere (atm), bar, millimeter mercury (mmHg) |
| **Angle**      | 📐    | degree (deg), radian (rad), gradian (grad)                          |
| **Digital**    | 💾    | byte (B), kilobyte (KB), megabyte (MB), gigabyte (GB), terabyte (TB), petabyte (PB), exabyte (EB) |

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- `pyTelegramBotAPI` library

Install the required library:

```bash
pip install pyTelegramBotAPI , pytz
```

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ItsReZNuM/UnitBot
   cd unitbot
   ```

2. **Set Up Your Bot Token**:

   - Create a new bot using [BotFather](https://t.me/BotFather) on Telegram.
   - Copy the bot token and replace `'YOUR_BOT_TOKEN'` in the `unit_converter_bot_fixed_units.py` file with your token.

3. **Configure BotFather Commands**:

   To enable `/start` and `/help` commands to appear when users type `/` in the bot chat:

   - Open a chat with @BotFather.
   - Send `/setcommands` and select your bot.
   - Paste the following:

     ```
     start - Start using the bot
     help - Display the full help guide
     ```

4. **Enable Inline Mode**:

   - In BotFather, send `/setinline` to enable inline mode for your bot.
   - Optionally, set a placeholder with `/setinlineplaceholder` (e.g., `10 kilometer`).

5. **Run the Bot**:

   ```bash
   python unit.py
   ```

## 🛠️ Usage

### Commands

- **/start**: Displays a bilingual welcome message with usage instructions.
- **/help**: Shows a detailed bilingual guide with supported units and examples.

### Inline Mode

Use the bot in any Telegram chat by typing:

```
@UnitBot <number> <unit>
```

- **Examples**:
  - `@UnitBot 10 km`: Converts 10 kilometers to all length units.
  - `@UnitBot 5 kg`: Converts 5 kilograms to all weight units.
  - `@UnitBot 1 cc`: Converts 1 cubic centimeter to all volume units.
  - `@UnitBot 1 KB`: Converts 1 kilobyte to all digital storage units.

### Input Format

- **Numbers**: Supports both English (e.g., `10`, `5.5`) and Persian numerals (e.g., `۱۰`, `۵.۵`).
- **Units**: Accepts full names (e.g., `kilometer`) or abbreviations (e.g., `km`), case-insensitive.
- **Spacing**: Ensure a space between the number and unit (e.g., `10 km`, not `10km`).

### Example Outputs

1. **Input**: `@UnitBot 1 cm`
   - **Output**:
     ```
     📏 1 cm = 0.00001 km
     📏 1 cm = 0.000006 mi
     📏 1 cm = 0.01 m
     📏 1 cm = 0.010936 yd
     📏 1 cm = 0.032808 ft
     📏 1 cm = 0.1 dm
     📏 1 cm = 0.39 in
     📏 1 cm = 10 mm
     ```

2. **Input**: `@UnitBot 1 KB`
   - **Output**:
     ```
     💾 1 KB = 1,024 B
     💾 1 KB = 0.000977 MB
     💾 1 KB = 0.000001 GB
     💾 1 KB = 0.000000001 TB
     💾 1 KB = 0.000000000001 PB
     💾 1 KB = 0.000000000000001 EB
     ```

3. **Input**: `@UnitBot 1 cc`
   - **Output**:
     ```
     🧴 1 cc = 1 ml
     🧴 1 cc = 1 cm3
     🧴 1 cc = 0.001 l
     🧴 1 cc = 0.000001 m3
     🧴 1 cc = 0.000264 gal
     🧴 1 cc = 0.000006 bbl
     ```

## 🐛 Debugging

- If the bot encounters an error, check the `bot.log` file in the project directory for details.
- Common issues:
  - Invalid bot token: Ensure the `TOKEN` in the script is correct.
  - Inline mode not enabled: Use `/setinline` in BotFather.
  - Formatting issues: Ensure inputs follow the correct format (e.g., `@UnitBot 10 km`).

## 🤝 Contributing

Contributions are welcome! 🎉 To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Please ensure your code follows the existing style and includes relevant tests.



## 📬 Contact

For questions or suggestions, feel free to open an issue or contact the maintainer via Telegram: [@MyTelegramID](https://t.me/ItsReZNuM).

Happy converting with UnitBot! 🎉