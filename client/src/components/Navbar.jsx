function Navbar(){
    return(
        <nav className="bg-slate-50 border-gray-200" id="navbar">
          <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
          <a href="index.html" className="flex items-center space-x-3 rtl:space-x-reverse">
          </a>
      
          <div className="flex items-center md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
      
            <button data-collapse-toggle="navbar-user" type="button" className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-user" aria-expanded="false">
                <svg className="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                    <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 1h15M1 7h15M1 13h15"/>
                </svg>
            </button>
          </div>
      
      <div className="justify-between hidden w-full md:flex md:w-auto md:order-1 items-center" id="navbar-user">
        <ul className="md:flex md:items-center flex-col font-medium p-4 mt-4 rounded-lg  md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0">
          <li>
            <a href="/" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0">Pesquisa</a>
          </li>
          <li>
            <a href="/noticias" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0">Noticias</a>
          </li>
          <li>
            <a href="/sobre" className="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0">Sobre</a>
          </li>
        </ul>
      </div>
      </div>
      </nav>
      
    )
}

export default Navbar