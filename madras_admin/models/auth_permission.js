'use strict';

module.exports = (sequelize, DataTypes) => {
  var Model = sequelize.define('auth_permission', {
    'content_type_id': {
      type: DataTypes.INTEGER,
    },
    'codename': {
      type: DataTypes.STRING,
    },
    'name': {
      type: DataTypes.STRING,
    },
  }, {
    tableName: 'auth_permission',
    underscored: true,
    timestamps: false,
    
  });

  Model.associate = (models) => {
  };

  return Model;
};

