import { SettingModal } from "../compoents/SettingModal";
import { ThemeSwitcher } from "../compoents/ThemeSwitch";

interface HeaderProps {
  title: string;
  image?: string;
}

export const Header = (props: HeaderProps) => {
  return (
    <header>
      <nav className="bg-white border-gray-200 px-4 lg:px-6 py-2.5 dark:bg-gray-800">
        <div className="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
          <span className="self-center text-xl font-semibold whitespace-nowrap dark:text-white">
            {props.title}
          </span>

          <div className="flex items-center lg:order-2">
            <div className="flex space-x-2">
              <ThemeSwitcher />
              <SettingModal />
            </div>
          </div>
          <div
            className="hidden justify-between items-center w-full lg:flex lg:w-auto lg:order-1"
            id="mobile-menu-2"
          ></div>
        </div>
      </nav>
    </header>
  );
};
